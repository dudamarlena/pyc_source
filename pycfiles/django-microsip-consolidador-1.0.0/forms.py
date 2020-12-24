# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\GitHub\django-microsip-base\django_microsip_base\django_microsip_base\apps\plugins\django-microsip-consolidador\django-microsip-consolidador\forms.py
# Compiled at: 2015-03-20 17:53:25
from django import forms
from .models import *
import autocomplete_light

class ArticuloSearchForm(forms.Form):
    articulo = forms.ModelChoiceField(queryset=Articulo.objects.all(), widget=autocomplete_light.ChoiceWidget('ArticuloAutocomplete'), required=False)
    clave = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'clave...'}), required=False)

    def clean(self, *args, **kwargs):
        cleaned_data = self.cleaned_data
        clave = cleaned_data.get('clave')
        articulo = cleaned_data.get('articulo')
        if articulo:
            clave = ''
        if not ArticuloClave.objects.filter(clave=clave).exists() and clave:
            raise forms.ValidationError('No existen articulos con esta clave')
        elif not clave and not articulo:
            raise forms.ValidationError('Seleciona un articulo por favor')
        return cleaned_data