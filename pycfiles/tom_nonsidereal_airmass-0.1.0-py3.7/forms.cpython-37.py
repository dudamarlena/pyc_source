# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tom_nonsidereal_airmass/forms.py
# Compiled at: 2019-09-20 20:05:55
# Size of source mod 2**32: 701 bytes
from django import forms
from django.forms import ValidationError

class NonsiderealTargetVisibilityForm(forms.Form):
    start_time = forms.DateTimeField(required=True, label='Start Time', widget=forms.TextInput(attrs={'type': 'date'}))
    end_time = forms.DateTimeField(required=True, label='End Time', widget=forms.TextInput(attrs={'type': 'date'}))
    airmass = forms.DecimalField(required=False, label='Maximum Airmass')

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        if end_time < start_time:
            raise forms.ValidationError('Start time must be before end time')