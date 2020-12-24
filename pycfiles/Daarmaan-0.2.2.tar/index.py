# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lxsameer/src/daarmaan/daarmaan/server/views/index.py
# Compiled at: 2012-10-13 07:58:26
from django.shortcuts import render_to_response as rr
from django.shortcuts import redirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.conf.urls import patterns, url
from django.conf import settings
from daarmaan.server.forms import PreRegistrationForm, NewUserForm
from daarmaan.server.models import VerificationCode

class IndexPage(object):
    """
    Daarmaan index page class.
    """
    template = 'index.html'
    new_user_form_template = 'new_user_form.html'

    @property
    def urls(self):
        """
        First Page url patterns.
        """
        urlpatterns = patterns('', url('^$', self.index, name='home'), url('^verificate/([A-Fa-f0-9]{40})/$', self.verificate, name='verificate'), url('^registration/done/$', self.registration_done, name='registration-done'))
        return urlpatterns

    def index(self, request):
        """
        Index view.
        """
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('dashboard-index'))
        else:
            if request.method == 'POST':
                return self.on_post(request)
            return self.on_get(request)

    def on_get(self, request):
        """
        This view handles GET requests.
        """
        form = PreRegistrationForm()
        next_url = request.GET.get('next', '')
        return rr(self.template, {'regform': form, 'next': next_url}, context_instance=RequestContext(request))

    def on_post(self, request):
        """
        This view handles POST requests.
        """
        if request.POST['form'] == 'login':
            return self.login(request)
        else:
            return self.pre_register(request)

    def login(self, request):
        """
        Login view that only accept a POST request.
        """
        username = request.POST['username']
        password = request.POST['password']
        remember = request.POST.get('remember_me', False)
        next_url = request.POST.get('next', None)
        form = PreRegistrationForm()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                self._setup_session(request)
                if next_url:
                    return HttpResponseRedirect(next_url)
                return redirect(reverse('dashboard-index', args=[]))
            else:
                return rr(self.template, {'regform': form, 'msgclass': 'error', 
                   'next': next_url, 
                   'msg': _('Your account is disabled.')}, context_instance=RequestContext(request))

        else:
            return rr(self.template, {'regform': form, 'msgclass': 'error', 
               'next': next_url, 
               'msg': _('Username or Password is invalid.')}, context_instance=RequestContext(request))
        return

    def pre_register(self, request):
        """
        Handle the registeration request.
        """
        from django.contrib.auth.models import User
        from django.db import IntegrityError
        form = PreRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            emails_count = User.objects.filter(email=email).count()
            if emails_count:
                failed = True
                msg = _('This email has been registered before.')
                klass = 'error'
            else:
                try:
                    user = User(username=username, email=email)
                    user.active = False
                    user.save()
                    if settings.EMAIL_VERIFICATION:
                        verif_code = VerificationCode.generate(user)
                        verification_link = reverse('verificate', args=[
                         verif_code])
                        print '>>> ', verification_link
                        self.send_verification_mail(user, verification_link)
                        msg = _('A verfication mail has been sent to your e-mail address.')
                    else:
                        msg = _("You're request submited, thanks for your interest.")
                    klass = 'info'
                    form = PreRegistrationForm()
                except IntegrityError:
                    msg = _('User already exists.')
                    klass = 'error'

        return rr(self.template, {'regform': form, 'msgclass': klass, 
           'msg': msg}, context_instance=RequestContext(request))

    def _setup_session(self, request):
        """
        Insert all needed values into user session.
        """
        return
        services = request.user.get_profile().services.all()
        services_id = [ i.id for i in services ]
        request.session['services'] = services_id

    def verificate(self, request, verification_code):
        """
        This view is responsible for verify the user mail address
        from the given verification code and redirect to the basic
        information form view.
        """
        try:
            verified_code = VerificationCode.objects.get(code=verification_code)
        except VerificationCode.DoesNotExist:
            raise Http404()

        if verified_code.is_valid():
            form = NewUserForm(initial={'verification_code': verified_code.code})
            form.action = reverse('registration-done', args=[])
            return rr(self.new_user_form_template, {'form': form, 'user': verified_code.user}, context_instance=RequestContext(request))
        raise Http404()

    def send_verification_mail(self, user, verification_link):
        """
        Send the verification link to the user.
        """
        from django.core.mail import send_mail
        msg = verification_link
        send_mail('[Yellowen] Verification', msg, settings.EMAIL, [
         user.email], fail_silently=False)

    def registration_done(self, request):
        if request.method == 'POST':
            form = NewUserForm(request.POST)
            try:
                verified_code = VerificationCode.objects.get(code=request.POST.get('verification_code', ''))
            except VerificationCode.DoesNotExist:
                return HttpResponseForbidden()

            if form.is_valid():
                pass1 = form.cleaned_data['password1']
                pass2 = form.cleaned_data['password2']
                fname = form.cleaned_data['first_name']
                lname = form.cleaned_data['last_name']
                if pass1 != pass2:
                    form._errors = {'password1': _('Two password fields did not match.'), 'password2': _('Two password fields did not match.')}
                    msg = _('Two password fields did not match.')
                    klass = 'error'
                elif len(pass1) < 6:
                    form._errors = {'password1': _('Password should be more than 6 character long.')}
                    msg = _('Password should be more than 6 character long.')
                    klass = 'error'
                elif len(pass1) > 40:
                    form._errors = {'password1': _('Password should be less than 40 character long.')}
                    msg = _('Password should be less than 40 character long.')
                    klass = 'error'
                else:
                    user = verified_code.user
                    user.set_password(pass1)
                    user.first_name = fname
                    user.last_name = lname
                    user.active = True
                    user.save()
                    verified_code.delete()
                    VerificationCode.cleanup()
                    user = authenticate(username=user.username, password=pass1)
                    login(request, user)
                    return redirect(reverse('dashboard-index', args=[]))
            return rr(self.new_user_form_template, {'form': form, 'user': verified_code.user, 
               'msg': msg, 
               'klass': klass}, context_instance=RequestContext(request))
        raise Http404()


index_page = IndexPage()