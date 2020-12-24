# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/suit/forms.py
# Compiled at: 2018-11-26 02:58:29
from __future__ import unicode_literals
import unicodedata
from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.utils.text import capfirst
from django.utils.translation import ugettext, ugettext_lazy as _
from aparnik.utils.utils import convert_iran_phone_number_to_world_number
from aparnik.settings import aparnik_settings
UserModel = get_user_model()

class UsernameField(forms.CharField):

    def to_python(self, value):
        return unicodedata.normalize(b'NFKC', super(UsernameField, self).to_python(value))


class AuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    username = UsernameField(max_length=254, widget=forms.TextInput(attrs={b'autofocus': True}))
    password = forms.CharField(label=_(b'Password'), strip=False, widget=forms.PasswordInput)
    step = 1
    error_messages = {b'invalid_login': _(b'Please enter a correct %(username)s and password. Note that both fields may be case-sensitive.'), 
       b'inactive': _(b'This account is inactive.')}

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        if self.fields[b'username'].label is None:
            self.fields[b'username'].label = capfirst(self.username_field.verbose_name)
        return

    def clean(self):
        username = self.cleaned_data.get(b'username')
        username = convert_iran_phone_number_to_world_number(username)
        password = self.cleaned_data.get(b'password')
        if username is not None and password is None:
            try:
                user = UserModel.objects.get(username=username)
                self.step = 2
                if not aparnik_settings.USER_LOGIN_WITH_PASSWORD:
                    user.OTARequest()
            except:
                raise forms.ValidationError(self.error_messages[b'invalid_login'], code=b'invalid_login', params={b'username': self.username_field.verbose_name})

        elif username is not None and password is not None:
            self.step = 2
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(self.error_messages[b'invalid_login'], code=b'invalid_login', params={b'username': self.username_field.verbose_name})
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``forms.ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise forms.ValidationError(self.error_messages[b'inactive'], code=b'inactive')

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        else:
            return

    def get_user(self):
        return self.user_cache