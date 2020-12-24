# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Ozgur/Dropbox/Sites/django-manifest/manifest/mixins.py
# Compiled at: 2019-10-15 15:40:16
# Size of source mod 2**32: 5201 bytes
""" Manifest View Mixins
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.generic import FormView, View
from manifest import decorators, defaults
from manifest.utils import get_protocol

class MessageMixin:
    __doc__ = '\n    View mixin adding messages to response.\n    '
    success_message = ''
    error_message = ''
    extra_context = None

    def set_success_message(self, message):
        if defaults.MANIFEST_USE_MESSAGES:
            messages.success((self.request), message, fail_silently=True)

    def set_error_message(self, message):
        if defaults.MANIFEST_USE_MESSAGES:
            messages.error((self.request), message, fail_silently=True)


class SendMailMixin:
    __doc__ = '\n    Mixin that send an email to given recipients.\n    '
    from_email = None
    email_subject_template_name = None
    email_message_template_name = None
    email_html_template_name = None

    def create_email(self, context, recipient):
        if not self.email_subject_template_name:
            raise ImproperlyConfigured('No template name for subject. Provide a email_subject_template_name.')
        if not self.email_message_template_name:
            raise ImproperlyConfigured('No template name for message. Provide a email_message_template_name.')
        subject = ''.join(render_to_string(self.email_subject_template_name, context).splitlines())
        message = render_to_string(self.email_message_template_name, context)
        return EmailMultiAlternatives(subject, message, self.from_email, [recipient])

    def send_mail(self, recipient, opts):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        context = {'protocol':get_protocol(), 
         'site':Site.objects.get_current()}
        context.update(opts)
        email = self.create_email(context, recipient)
        if self.email_html_template_name is not None:
            html_email = render_to_string(self.email_html_template_name, context)
            email.attach_alternative(html_email, 'text/html')
        return email.send()


class SendActivationMailMixin(SendMailMixin):

    def send_activation_mail(self, user):
        context = {'user':user, 
         'activation_days':defaults.MANIFEST_ACTIVATION_DAYS, 
         'activation_key':user.activation_key}
        self.send_mail(user.email, context)


class EmailChangeMixin(SendMailMixin):
    email_subject_template_name_old = 'manifest/emails/confirmation_email_subject_old.txt'
    email_message_template_name_old = 'manifest/emails/confirmation_email_message_old.txt'
    email_html_template_name_old = None
    email_subject_template_name_new = 'manifest/emails/confirmation_email_subject_new.txt'
    email_message_template_name_new = 'manifest/emails/confirmation_email_message_new.txt'
    email_html_template_name_new = None

    def send_confirmation_mail(self, user):
        context = {'user':user, 
         'new_email':user.email_unconfirmed, 
         'confirmation_key':user.email_confirmation_key}
        self.email_subject_template_name = self.email_subject_template_name_old
        self.email_message_template_name = self.email_message_template_name_old
        self.email_html_template_name = self.email_html_template_name_old
        self.send_mail(user.email, context)
        self.email_subject_template_name = self.email_subject_template_name_new
        self.email_message_template_name = self.email_message_template_name_new
        self.email_html_template_name = self.email_html_template_name_new
        self.send_mail(user.email_unconfirmed, context)


class SecureRequiredMixin(View):
    __doc__ = '\n    Mixin that switches URL from http to https if\n    ``MANIFEST_USE_HTTPS`` setting is ``True``.\n\n    '

    @method_decorator(decorators.secure_required)
    def dispatch(self, request, *args, **kwargs):
        return (super().dispatch)(request, *args, **kwargs)


class LoginRequiredMixin(View):
    __doc__ = '\n    Mixin that redirects user to login form if not authenticated yet.\n\n    '

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return (super().dispatch)(request, *args, **kwargs)


class UserFormMixin(FormView, SecureRequiredMixin, LoginRequiredMixin, MessageMixin):
    __doc__ = '\n    Mixin that sets forms user argument to ``request.user``.\n    '

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs