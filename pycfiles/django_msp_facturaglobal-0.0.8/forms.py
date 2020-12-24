# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SIC2-U\Documents\GitHub\django-microsip-base\django_microsip_base\django_microsip_base\apps\plugins\django_msp_facturaglobal\django_msp_facturaglobal\forms.py
# Compiled at: 2014-12-10 16:41:50
from django import forms
import autocomplete_light
from .models import *

class DateRangeForm(forms.Form):
    start_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'fecha inicio...'}), required=True)
    end_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'fecha fin...'}), required=True)
    cliente = forms.ModelChoiceField(Cliente.objects.all(), widget=autocomplete_light.ChoiceWidget('ClienteAutocomplete'), required=True)

    def clean(self, *args, **kwargs):
        cleaned_data = self.cleaned_data
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date and end_date:
            if start_date.month != end_date.month:
                raise forms.ValidationError('Ambas fechas deben de ser del mismo mes')
        return cleaned_data