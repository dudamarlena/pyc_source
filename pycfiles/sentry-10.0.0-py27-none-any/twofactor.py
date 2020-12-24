# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/web/frontend/twofactor.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
import six, time
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.translation import ugettext as _
from sentry import options
from sentry.app import ratelimiter
from sentry.web.frontend.base import BaseView
from sentry.web.forms.accounts import TwoFactorForm
from sentry.web.helpers import render_to_response
from sentry.utils import auth, json
from sentry.models import Authenticator
COOKIE_NAME = 's2fai'
COOKIE_MAX_AGE = 2678400

class TwoFactorAuthView(BaseView):
    auth_required = False

    def perform_signin(self, request, user, interface=None):
        if not auth.login(request, user, passed_2fa=True):
            raise AssertionError
            rv = HttpResponseRedirect(auth.get_login_redirect(request))
            if interface is not None:
                interface.authenticator.mark_used()
                interface.is_backup_interface or rv.set_cookie(COOKIE_NAME, six.text_type(interface.type).encode('utf-8'), max_age=COOKIE_MAX_AGE, path='/')
        return rv

    def fail_signin(self, request, user, form):
        time.sleep(2.0)
        form.errors['__all__'] = [_('Invalid confirmation code. Try again.')]

    def negotiate_interface(self, request, interfaces):
        if len(interfaces) == 1:
            return interfaces[0]
        interface_id = request.GET.get('interface')
        if interface_id:
            for interface in interfaces:
                if interface.interface_id == interface_id:
                    return interface

        interface_type = request.COOKIES.get(COOKIE_NAME)
        if interface_type:
            for interface in interfaces:
                if six.text_type(interface.type) == interface_type:
                    return interface

        return interfaces[0]

    def get_other_interfaces(self, selected, all):
        rv = []
        can_validate_otp = selected.can_validate_otp
        backup_interface = None
        for idx, interface in enumerate(all):
            if interface.interface_id == selected.interface_id:
                continue
            if idx == 0 or interface.requires_activation:
                rv.append(interface)
                if interface.can_validate_otp:
                    can_validate_otp = True
            if backup_interface is None and interface.can_validate_otp and interface.is_backup_interface:
                backup_interface = interface

        if not can_validate_otp and backup_interface is not None:
            rv.append(backup_interface)
        return rv

    def validate_otp(self, otp, selected_interface, all_interfaces=None):
        if selected_interface.validate_otp(otp):
            return selected_interface
        for interface in all_interfaces or ():
            if interface.interface_id != selected_interface.interface_id and interface.is_backup_interface and interface.validate_otp(otp):
                return interface

    def handle(self, request):
        user = auth.get_pending_2fa_user(request)
        if user is None:
            return HttpResponseRedirect(auth.get_login_url())
        else:
            interfaces = Authenticator.objects.all_interfaces_for_user(user)
            if not interfaces:
                return self.perform_signin(request, user)
            challenge = activation = None
            interface = self.negotiate_interface(request, interfaces)
            if request.method == 'POST' and ratelimiter.is_limited(('auth-2fa:user:{}').format(user.id), limit=5, window=60):
                return HttpResponse('You have made too many 2FA attempts. Please try again later.', content_type='text/plain', status=429)
            if request.method == 'GET':
                activation = interface.activate(request)
                if activation is not None and activation.type == 'challenge':
                    challenge = activation.challenge
            elif 'challenge' in request.POST:
                challenge = json.loads(request.POST['challenge'])
            form = TwoFactorForm()
            otp = request.POST.get('otp')
            if otp:
                used_interface = self.validate_otp(otp, interface, interfaces)
                if used_interface is not None:
                    return self.perform_signin(request, user, used_interface)
                self.fail_signin(request, user, form)
            if challenge:
                response = request.POST.get('response')
                if response:
                    response = json.loads(response)
                    if interface.validate_response(request, challenge, response):
                        return self.perform_signin(request, user, interface)
                    self.fail_signin(request, user, form)
            return render_to_response([
             'sentry/twofactor_%s.html' % interface.interface_id, 'sentry/twofactor.html'], {'form': form, 
               'interface': interface, 
               'other_interfaces': self.get_other_interfaces(interface, interfaces), 
               'activation': activation}, request, status=200)


def u2f_appid(request):
    facets = options.get('u2f.facets')
    if not facets:
        facets = [
         options.get('system.url-prefix')]
    return HttpResponse(json.dumps({'trustedFacets': [{'version': {'major': 1, 'minor': 0}, 'ids': [ x.rstrip('/') for x in facets ]}]}), content_type='application/fido.trusted-apps+json')