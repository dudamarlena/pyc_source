# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pratheek/msc/pythons/lib/python3.5/site-packages/simpleauth/forms.py
# Compiled at: 2017-02-09 05:20:29
# Size of source mod 2**32: 429 bytes
from django import forms
from .models import Users

class StartForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Users
        fields = ('username', 'password')