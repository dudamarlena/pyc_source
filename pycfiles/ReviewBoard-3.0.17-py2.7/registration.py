# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/accounts/forms/registration.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from django import forms
from djblets.auth.forms import RegistrationForm as DjbletsRegistrationForm
from djblets.recaptcha.mixins import RecaptchaFormMixin
from djblets.siteconfig.models import SiteConfiguration
from reviewboard.accounts.mixins import PolicyConsentFormMixin

class RegistrationForm(RecaptchaFormMixin, PolicyConsentFormMixin, DjbletsRegistrationForm):
    """A registration form with reCAPTCHA support.

    This is a version of the Djblets RegistrationForm which knows how to
    validate a reCAPTCHA widget. Any error received is stored in the form
    for use when generating the widget so that the widget can properly display
    the error.
    """
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    def save(self):
        """Save the form."""
        user = DjbletsRegistrationForm.save(self)
        if user:
            user.first_name = self.cleaned_data[b'first_name']
            user.last_name = self.cleaned_data[b'last_name']
            user.save()
            self.accept_policies(user)
        return user

    @property
    def verify_recaptcha(self):
        siteconfig = SiteConfiguration.objects.get_current()
        return siteconfig.get(b'auth_registration_show_captcha')