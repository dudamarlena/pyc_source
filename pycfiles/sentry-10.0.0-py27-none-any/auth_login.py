# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/web/frontend/auth_login.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import never_cache
from sentry.auth.superuser import is_active_superuser
from sentry.constants import WARN_SESSION_EXPIRED
from sentry.http import get_server_hostname
from sentry.models import AuthProvider, Organization, OrganizationStatus
from sentry.web.forms.accounts import AuthenticationForm, RegistrationForm
from sentry.web.frontend.base import BaseView
from sentry.utils import auth, metrics
from sentry.utils.sdk import capture_exception
ERR_NO_SSO = _('The organization does not exist or does not have Single Sign-On enabled.')

class AdditionalContext(object):

    def __init__(self):
        self._callbacks = set()

    def add_callback(self, callback):
        """callback should take a request object and return a dict of key-value pairs
        to add to the context."""
        self._callbacks.add(callback)

    def run_callbacks(self, request):
        context = {}
        for cb in self._callbacks:
            try:
                result = cb(request)
                context.update(result)
            except Exception:
                capture_exception()

        return context


additional_context = AdditionalContext()

class AuthLoginView(BaseView):
    auth_required = False

    def get_auth_provider(self, organization_slug):
        try:
            organization = Organization.objects.get(slug=organization_slug, status=OrganizationStatus.VISIBLE)
        except Organization.DoesNotExist:
            return

        try:
            auth_provider = AuthProvider.objects.get(organization=organization)
        except AuthProvider.DoesNotExist:
            return

        return auth_provider

    def get_login_form(self, request):
        op = request.POST.get('op')
        return AuthenticationForm(request, request.POST if op == 'login' else None)

    def get_register_form(self, request, initial=None):
        op = request.POST.get('op')
        return RegistrationForm(request.POST if op == 'register' else None, initial=initial)

    def can_register(self, request):
        return bool(auth.has_user_registration() or request.session.get('can_register'))

    def get_next_uri(self, request):
        next_uri_fallback = None
        if request.session.get('_next') is not None:
            next_uri_fallback = request.session.pop('_next')
        return request.GET.get(REDIRECT_FIELD_NAME, next_uri_fallback)

    def respond_login(self, request, context, **kwargs):
        return self.respond('sentry/login.html', context)

    def handle_basic_auth(self, request, **kwargs):
        can_register = self.can_register(request)
        op = request.POST.get('op')
        organization = kwargs.pop('organization', None)
        if not op:
            if '/register' in request.path_info and can_register:
                op = 'register'
            elif request.GET.get('op') == 'sso':
                op = 'sso'
        login_form = self.get_login_form(request)
        if can_register:
            register_form = self.get_register_form(request, initial={'username': request.session.get('invite_email', '')})
        else:
            register_form = None
        if can_register and register_form.is_valid():
            user = register_form.save()
            user.send_confirm_emails(is_new_user=True)
            user.backend = settings.AUTHENTICATION_BACKENDS[0]
            auth.login(request, user, organization_id=organization.id if organization else None)
            request.session.pop('can_register', None)
            request.session.pop('invite_email', None)
            return self.redirect(auth.get_login_redirect(request))
        else:
            if request.method == 'POST':
                from sentry.app import ratelimiter
                from sentry.utils.hashlib import md5_text
                login_attempt = op == 'login' and request.POST.get('username') and request.POST.get('password')
                if login_attempt and ratelimiter.is_limited(('auth:login:username:{}').format(md5_text(request.POST['username'].lower()).hexdigest()), limit=10, window=60):
                    login_form.errors['__all__'] = [
                     'You have made too many login attempts. Please try again later.']
                    metrics.incr('login.attempt', instance='rate_limited', skip_internal=True, sample_rate=1.0)
                else:
                    if login_form.is_valid():
                        user = login_form.get_user()
                        auth.login(request, user, organization_id=organization.id if organization else None)
                        metrics.incr('login.attempt', instance='success', skip_internal=True, sample_rate=1.0)
                        if not user.is_active:
                            return self.redirect(reverse('sentry-reactivate-account'))
                        return self.redirect(auth.get_login_redirect(request))
                    metrics.incr('login.attempt', instance='failure', skip_internal=True, sample_rate=1.0)
            context = {'op': op or 'login', 
               'server_hostname': get_server_hostname(), 
               'login_form': login_form, 
               'organization': organization, 
               'register_form': register_form, 
               'CAN_REGISTER': can_register}
            context.update(additional_context.run_callbacks(request))
            return self.respond_login(request, context, **kwargs)

    def handle_authenticated(self, request):
        next_uri = self.get_next_uri(request)
        if auth.is_valid_redirect(next_uri, host=request.get_host()):
            return self.redirect(next_uri)
        return self.redirect_to_org(request)

    @never_cache
    @transaction.atomic
    def handle(self, request, *args, **kwargs):
        return super(AuthLoginView, self).handle(request, *args, **kwargs)

    def get(self, request, **kwargs):
        next_uri = self.get_next_uri(request)
        if request.user.is_authenticated():
            if not request.user.is_superuser or is_active_superuser(request):
                return self.handle_authenticated(request)
        request.session.set_test_cookie()
        auth.initiate_login(request, next_uri)
        if settings.SENTRY_SINGLE_ORGANIZATION:
            org = Organization.get_default()
            next_uri = reverse('sentry-auth-organization', args=[org.slug])
            return HttpResponseRedirect(next_uri)
        session_expired = 'session_expired' in request.COOKIES
        if session_expired:
            messages.add_message(request, messages.WARNING, WARN_SESSION_EXPIRED)
        response = self.handle_basic_auth(request, **kwargs)
        if session_expired:
            response.delete_cookie('session_expired')
        return response

    def post(self, request, **kwargs):
        op = request.POST.get('op')
        if op == 'sso' and request.POST.get('organization'):
            auth_provider = self.get_auth_provider(request.POST['organization'])
            if auth_provider:
                next_uri = reverse('sentry-auth-organization', args=[request.POST['organization']])
            else:
                next_uri = request.get_full_path()
                messages.add_message(request, messages.ERROR, ERR_NO_SSO)
            return HttpResponseRedirect(next_uri)
        return self.handle_basic_auth(request, **kwargs)