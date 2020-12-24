# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\FilePkl\latihan_django\11agustus\djangoproj\form\forms.py
# Compiled at: 2014-08-18 01:26:54
from django.forms import ModelForm
from .models import ContactForm
from django import forms

class ContactView(ModelForm):
    message = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = ContactForm