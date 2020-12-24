# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: M:\Programming\Project\django-auth\auth\CustomAuth\forms\user_forms.py
# Compiled at: 2020-01-28 13:32:35
# Size of source mod 2**32: 2659 bytes
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm, UsernameField
from models.user import User

class UserCreationForm(forms.ModelForm):
    __doc__ = '\n    A form for creating new users. Includes all the required fields, plus a repeated password.\n    '
    password1 = forms.CharField(label='Password', widget=(forms.PasswordInput))
    password2 = forms.CharField(label='Password confirmation', widget=(forms.PasswordInput))

    class Meta:
        model = User
        fields = ('email', )

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1:
            if password2:
                if password1 != password2:
                    raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password1'))
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    __doc__ = "A form for updating users. Includes all the fields on\n    the user, but replaces the password field with admin's\n    password hash display field.\n    "
    password = ReadOnlyPasswordHashField(label='Password',
      help_text='Raw passwords are not stored, so there is no way to see this user\'s password, but you can change the password using <a href="../password/">this form</a>.')

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'is_superuser', 'is_staff',
                  'is_verify', 'is_active', 'user_permissions', 'groups', 'date_verify')

    def clean_password(self):
        return self.initial['password']


class UserLoginForm(AuthenticationForm):
    user_attr = {'autofocus':True, 
     'class':''}
    pass_attr = {'class': ''}
    username = UsernameField(widget=forms.TextInput(attrs=user_attr))
    password = forms.CharField(label='Password',
      strip=False,
      widget=forms.PasswordInput(attrs=pass_attr))