# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Ozgur/Dropbox/Sites/django-manifest/manifest/views.py
# Compiled at: 2019-10-15 15:40:16
# Size of source mod 2**32: 11308 bytes
""" Manifest Views
"""
from django.contrib.auth import REDIRECT_FIELD_NAME, get_user_model, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView, LogoutView
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import CreateView, DetailView, ListView, TemplateView, UpdateView
from manifest import defaults, messages, signals
from manifest.forms import EmailChangeForm, LoginForm, ProfileUpdateForm, RegisterForm
from manifest.mixins import EmailChangeMixin, LoginRequiredMixin, MessageMixin, SecureRequiredMixin, SendActivationMailMixin, UserFormMixin
from manifest.utils import get_login_redirect

@method_decorator((sensitive_post_parameters('password')), name='dispatch')
class AuthLoginView(LoginView, SecureRequiredMixin, MessageMixin):
    __doc__ = 'Authenticate user by email or username with password.\n\n    If the credentials are correct and the user ``is_active``,\n    user will be redirected to ``success_url`` if it is defined.\n\n    If ``success_url`` is not defined, the ``login_redirect`` function\n    will be called with the arguments ``REDIRECT_FIELD_NAME`` and an\n    instance of the ``User`` who is trying the login. The returned\n    value of the function will be the URL that will be redirected to.\n    '
    form_class = LoginForm
    template_name = 'manifest/auth_login.html'
    success_message = messages.AUTH_LOGIN_SUCCESS
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.get_user()
        if user.is_active:
            login(self.request, user)
            self.request.session.set_expiry(defaults.MANIFEST_REMEMBER_DAYS[1] * 86400)
            self.set_success_message(self.success_message)
            if self.success_url:
                return redirect(self.success_url)
            url = get_login_redirect(self.request.GET.get(REDIRECT_FIELD_NAME, self.request.POST.get(REDIRECT_FIELD_NAME)))
            return redirect(url)
        return redirect(reverse('auth_disabled'))


class AuthLogoutView(LogoutView, MessageMixin):
    __doc__ = 'Django ``LogoutView`` wrapper.\n\n    Display a success message if ``MANIFEST_USE_MESSAGES`` setting is ``True``\n    '
    template_name = 'manifest/auth_logout.html'
    success_message = messages.AUTH_LOGOUT_SUCCESS

    def dispatch(self, request, *args, **kwargs):
        self.set_success_message(self.success_message)
        return (super().dispatch)(request, *args, **kwargs)


@method_decorator((sensitive_post_parameters('password1', 'password2')),
  name='dispatch')
class AuthRegisterView(CreateView, SecureRequiredMixin, MessageMixin, SendActivationMailMixin):
    __doc__ = 'Register user with username, email and password.\n\n    Users receives an email with an activation link to activate their\n    account if ``MANIFEST_ACTIVATION_REQUIRED`` setting is ``True``.\n\n    Redirects to ``success_url`` if it is defined, else redirects to\n    ``auth_register_complete`` view.\n    '
    model = get_user_model()
    form_class = RegisterForm
    template_name = 'manifest/auth_register.html'
    success_message = messages.AUTH_REGISTER_SUCCESS
    redirect_authenticated_user = True
    email_subject_template_name = 'manifest/emails/activation_email_subject.txt'
    email_message_template_name = 'manifest/emails/activation_email_message.txt'

    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user:
            if request.user.is_authenticated:
                return redirect(get_login_redirect(self.request.GET.get(REDIRECT_FIELD_NAME, self.request.POST.get(REDIRECT_FIELD_NAME))))
        return (super().dispatch)(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        signals.REGISTRATION_COMPLETE.send(sender=None,
          user=user,
          request=(self.request))
        if defaults.MANIFEST_ACTIVATION_REQUIRED:
            self.send_activation_mail(user)
        self.set_success_message(self.success_message)
        if self.success_url:
            return redirect(self.success_url)
        return redirect(reverse('auth_register_complete'))


class AuthActivateView(TemplateView, MessageMixin):
    __doc__ = 'Activate the user with the activation token.\n\n    The token is a SHA1 string. When the SHA1 is found with username\n    the ``User`` of that account will be activated.\n\n    After a successfull activation user will be redirected to\n    ``profile_settings`` view if ``succes_url`` is not defined.\n\n    If the SHA1 is not found, the user will be shown the\n    ``template_name`` template that displaying a fail message.\n    '
    template_name = 'manifest/auth_activate.html'
    success_message = messages.AUTH_ACTIVATE_SUCCESS
    error_message = messages.AUTH_ACTIVATE_ERROR
    success_url = None

    def get_success_url(self, **kwargs):
        if self.success_url:
            return self.success_url % kwargs
        return reverse('profile_settings')

    def get(self, request, *args, **kwargs):
        user = get_user_model().objects.activate_user(kwargs['username'], kwargs['token'])
        if user:
            login(request,
              user, backend='manifest.backends.AuthenticationBackend')
            self.set_success_message(self.success_message)
            return redirect((self.get_success_url)(**kwargs))
        self.set_error_message(self.error_message)
        return (super().get)(request, *args, **kwargs)


class AuthProfileView(DetailView, LoginRequiredMixin):
    __doc__ = 'Detail view for current user account\n\n    Simple detail view gets ``request.user`` as object.\n    '
    template_name = 'manifest/user_detail.html'

    def get_object(self, queryset=None):
        return self.request.user


class ProfileUpdateView(UpdateView, SecureRequiredMixin, LoginRequiredMixin, MessageMixin):
    __doc__ = 'Update profile of current user\n\n    Updates profile information for ``request.user``. User will be\n    redirected to ``profile_settings`` if ``success_url`` is not defined.\n    '
    model = get_user_model()
    form_class = ProfileUpdateForm
    template_name = 'manifest/profile_update.html'
    success_message = messages.PROFILE_UPDATE_SUCCESS

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        form.save()
        self.set_success_message(self.success_message)
        if self.success_url:
            return redirect(self.success_url)
        return redirect(reverse('profile_settings'))


class EmailChangeView(UserFormMixin, EmailChangeMixin):
    __doc__ = 'Change email of current user\n\n    Changes email for ``request.user``. Change will not be applied\n    until user confirm their new email.\n\n    User will be redirected to ``email_change_done`` view\n    if ``success_url`` is not defined.\n    '
    form_class = EmailChangeForm
    template_name = 'manifest/email_change.html'
    success_message = messages.EMAIL_CHANGE_SUCCESS

    def form_valid(self, form):
        user = form.save()
        self.send_confirmation_mail(user)
        self.set_success_message(self.success_message)
        if self.success_url:
            return redirect(self.success_url)
        return redirect(reverse('email_change_done'))


class EmailChangeConfirmView(TemplateView, MessageMixin):
    __doc__ = 'Confirm the email address with username and confirmation token.\n\n    Confirms the new email address by running\n    ``get_user_model().objects.confirm_email`` method.\n\n    User will be redirected to ``email_change_complete`` view\n    if ``success_url`` is not defined.\n\n    If no ``User`` object returned, user will be shown the\n    ``template_name`` template that displaying a fail message.\n    '
    template_name = 'manifest/email_change_confirm.html'
    success_message = messages.EMAIL_CHANGE_CONFIRM_SUCCESS
    error_message = messages.EMAIL_CHANGE_CONFIRM_ERROR
    success_url = None

    def get_success_url(self, **kwargs):
        if self.success_url:
            return self.success_url % kwargs
        return reverse('email_change_complete')

    def get(self, request, *args, **kwargs):
        user = get_user_model().objects.confirm_email(kwargs['username'], kwargs['token'])
        if user:
            self.set_success_message(self.success_message)
            return redirect((self.get_success_url)(**kwargs))
        self.set_error_message(self.error_message)
        return (super().get)(request, *args, **kwargs)


@method_decorator((sensitive_post_parameters()), name='dispatch')
class PasswordChangeView(UserFormMixin):
    __doc__ = 'Change password of current user.\n\n    Changes password for ``request.user``. User will be redirected to\n    ``password_change_done`` view if ``success_url`` is not defined.\n    '
    form_class = PasswordChangeForm
    template_name = 'manifest/password_change.html'
    success_message = messages.PASSWORD_CHANGE_SUCCESS

    def form_valid(self, form):
        user = form.save()
        signals.PASSWORD_RESET_COMPLETE.send(sender=None, user=user)
        self.set_success_message(self.success_message)
        update_session_auth_hash(self.request, user)
        if self.success_url:
            return redirect(self.success_url)
        return redirect(reverse('password_change_done'))


class UserListView(ListView):
    __doc__ = 'Lists active user profiles.\n\n    List view that lists active user profiles\n    if ``MANIFEST_DISABLE_PROFILE_LIST`` setting is ``False``,\n    else raises Http404.\n    '
    queryset = get_user_model().objects.get_visible_profiles()
    template_name = 'manifest/user_list.html'
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        if defaults.MANIFEST_DISABLE_PROFILE_LIST:
            if not request.user.is_superuser:
                raise Http404
        return (super().dispatch)(request, *args, **kwargs)


class UserDetailView(DetailView):
    __doc__ = 'Displays an active user profile by username.\n\n    Detail view that displays an active user profile by username.\n    if ``MANIFEST_DISABLE_PROFILE_LIST`` setting is ``False``,\n    else raises Http404.\n    '
    queryset = get_user_model().objects.get_visible_profiles()
    template_name = 'manifest/user_detail.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def dispatch(self, request, *args, **kwargs):
        if defaults.MANIFEST_DISABLE_PROFILE_LIST:
            if not request.user.is_superuser:
                raise Http404
        return (super().dispatch)(request, *args, **kwargs)