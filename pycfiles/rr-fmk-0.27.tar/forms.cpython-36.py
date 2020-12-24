# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rramos/00P/01-dajngo/3d/app/usuarios/forms.py
# Compiled at: 2018-03-27 13:02:38
# Size of source mod 2**32: 546 bytes
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, label='Nombre', required=True)
    last_name = forms.CharField(max_length=30, label='Apellido', required=True)
    email = forms.EmailField(max_length=254, help_text='Requiere una direccion valida de mail')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')