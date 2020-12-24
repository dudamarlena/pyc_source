# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /mnt/1T/home/Projects/django-email-as-username/emailusernames/forms.py
# Compiled at: 2015-11-06 09:38:12
# Size of source mod 2**32: 4871 bytes
from django import forms, VERSION
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from emailusernames.utils import user_exists
ERROR_MESSAGE = _('Please enter a correct email and password. ')
ERROR_MESSAGE_RESTRICTED = _('You do not have permission to access the admin.')
ERROR_MESSAGE_INACTIVE = _('This account is inactive.')

class EmailAuthenticationForm(AuthenticationForm):
    """EmailAuthenticationForm"""
    email = forms.EmailField(label=_('Email'), max_length=75)
    message_incorrect_password = ERROR_MESSAGE
    message_inactive = ERROR_MESSAGE_INACTIVE

    def __init__(self, request=None, *args, **kwargs):
        super(EmailAuthenticationForm, self).__init__(request, *args, **kwargs)
        if self.fields.get('username'):
            del self.fields['username']
        if hasattr(self.fields, 'keyOrder'):
            self.fields.keyOrder = ['email', 'password']
        else:
            from collections import OrderedDict
            fields = OrderedDict()
            for key in ('email', 'password'):
                fields[key] = self.fields.pop(key)

            for key, value in self.fields.items():
                fields[key] = value

            self.fields = fields

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            self.user_cache = authenticate(email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(self.message_incorrect_password)
            if not self.user_cache.is_active:
                raise forms.ValidationError(self.message_inactive)
        if hasattr(self, 'check_for_test_cookie'):
            self.check_for_test_cookie()
        return self.cleaned_data


class EmailAdminAuthenticationForm(AdminAuthenticationForm):
    """EmailAdminAuthenticationForm"""
    email = forms.EmailField(label=_('Email'), max_length=75)
    message_incorrect_password = ERROR_MESSAGE
    message_inactive = ERROR_MESSAGE_INACTIVE
    message_restricted = ERROR_MESSAGE_RESTRICTED

    def __init__(self, *args, **kwargs):
        super(EmailAdminAuthenticationForm, self).__init__(*args, **kwargs)
        if self.fields.get('username'):
            del self.fields['username']

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            self.user_cache = authenticate(email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(self.message_incorrect_password)
            if not self.user_cache.is_active:
                raise forms.ValidationError(self.message_inactive)
            if not self.user_cache.is_staff:
                raise forms.ValidationError(self.message_restricted)
        self.check_for_test_cookie()
        return self.cleaned_data


class EmailUserCreationForm(UserCreationForm):
    """EmailUserCreationForm"""
    email = forms.EmailField(label=_('Email'), max_length=75)

    class Meta:
        model = User
        fields = ('email', )

    def __init__(self, *args, **kwargs):
        super(EmailUserCreationForm, self).__init__(*args, **kwargs)
        if self.fields.get('username'):
            del self.fields['username']

    def clean_email(self):
        email = self.cleaned_data['email']
        if user_exists(email):
            raise forms.ValidationError(_('A user with that email already exists.'))
        return email

    def save(self, commit=True):
        self.instance.username = self.instance.email
        return super(EmailUserCreationForm, self).save(commit=commit)


class EmailUserChangeForm(UserChangeForm):
    """EmailUserChangeForm"""
    email = forms.EmailField(label=_('Email'), max_length=75)

    class Meta:
        model = User
        if VERSION[1] > 7:
            fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EmailUserChangeForm, self).__init__(*args, **kwargs)
        if self.fields.get('username'):
            del self.fields['username']