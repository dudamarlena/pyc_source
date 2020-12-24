# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shodh/Projects/django_ginger/ginger/staging/forms.py
# Compiled at: 2014-10-05 23:08:36
from django import forms
from ginger.staging import conf

class StagingForm(forms.Form):
    secret = forms.CharField(max_length=128)

    def clean_secret(self):
        value = self.cleaned_data['secret']
        if value != conf.STAGING_SECRET:
            raise forms.ValidationError('Oops! you have entered an invalid secret. Please try again')
        return value