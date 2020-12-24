# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./webapp/registration/forms.py
# Compiled at: 2014-06-01 18:18:49
from django import forms
from django.contrib.auth import forms as auth_forms
from mirskutils.registration.forms import EmailPasswordMixin, ConfirmPasswordMixin
from .models import Individual

class SignupForm(EmailPasswordMixin, ConfirmPasswordMixin):
    pass


class AccountForm(forms.ModelForm):

    class Meta:
        model = Individual
        fields = ('first_name', 'last_name', 'email')