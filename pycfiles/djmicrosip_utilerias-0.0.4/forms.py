# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\GitHub\django-microsip-base\django_microsip_base\django_microsip_base\apps\plugins\djmicrosip_utilerias\djmicrosip_utilerias\forms.py
# Compiled at: 2015-03-07 12:47:31
from django import forms
from django.contrib.auth import authenticate

class PasswordConfirmationForm(forms.Form):
    sysdba_password = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'password de SYSDBA...'}))

    def clean_sysdba_password(self, *args, **kwargs):
        sysdba_password = self.cleaned_data['sysdba_password']
        usuario = authenticate(username='SYSDBA', password=sysdba_password)
        if not usuario:
            raise forms.ValidationError('contraseña invalida')
        return sysdba_password