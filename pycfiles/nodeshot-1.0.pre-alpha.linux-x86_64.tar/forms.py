# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/community/profiles/forms.py
# Compiled at: 2015-03-02 10:21:03
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import PasswordReset
from .settings import EMAIL_CONFIRMATION
__all__ = [
 'ResetPasswordForm',
 'ResetPasswordKeyForm']

class ResetPasswordForm(forms.Form):
    email = forms.EmailField(label=_('Email'), required=True, widget=forms.TextInput(attrs={'size': '30'}))

    def clean_email(self):
        """ ensure email is in the database """
        if EMAIL_CONFIRMATION:
            from .models import EmailAddress
            condition = EmailAddress.objects.filter(email__iexact=self.cleaned_data['email'], verified=True).count() == 0
        else:
            condition = User.objects.get(email__iexact=self.cleaned_data['email'], is_active=True).count() == 0
        if condition is True:
            raise forms.ValidationError(_('Email address not verified for any user account'))
        return self.cleaned_data['email']

    def save(self, **kwargs):
        PasswordReset.objects.create_for_user(self.cleaned_dat['email'])
        return self.cleaned_data['email']


class ResetPasswordKeyForm(forms.Form):
    password1 = forms.CharField(label=_('New Password'), widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(label=_('New Password (again)'), widget=forms.PasswordInput(render_value=False))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.temp_key = kwargs.pop('temp_key', None)
        super(ResetPasswordKeyForm, self).__init__(*args, **kwargs)
        return

    def clean_password2(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_('Password confirmation mismatch.'))
        return self.cleaned_data['password2']

    def save(self):
        user = self.user
        user.set_password(self.cleaned_data['password1'])
        user.save()
        PasswordReset.objects.filter(temp_key=self.temp_key).update(reset=True)