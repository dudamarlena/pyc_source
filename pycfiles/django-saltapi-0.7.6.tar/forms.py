# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/code/django-saltapi/django_saltapi/forms.py
# Compiled at: 2013-03-11 11:22:01
from django import forms

class LowdataForm(forms.Form):
    client = forms.CharField(max_length=20, initial='local', widget=forms.HiddenInput())
    tgt = forms.CharField(max_length=50, label='Target')
    fun = forms.CharField(max_length=30, label='Module')
    arg = forms.CharField(max_length=100, required=False, label='Arguments')

    def clean(self):
        cleaned_data = super(LowdataForm, self).clean()
        return cleaned_data