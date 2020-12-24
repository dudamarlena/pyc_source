# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\GitHub\django-microsip-base\django_microsip_base\django_microsip_base\apps\plugins\djmicrosip_remgencargos\djmicrosip_remgencargos\forms.py
# Compiled at: 2015-02-27 17:25:34
from django import forms
from .models import *
import autocomplete_light

class SearchForm(forms.Form):
    inicio = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'inicio...'}), required=False)
    fin = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'fin...'}), required=False)
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), widget=autocomplete_light.ChoiceWidget('ClienteAutocomplete'), required=False)