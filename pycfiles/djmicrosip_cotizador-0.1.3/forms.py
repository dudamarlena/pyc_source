# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SIC2-U\Documents\GitHub\django-microsip-base\django_microsip_base\django_microsip_base\apps\plugins\djmicrosip_cotizador\djmicrosip_cotizador\forms.py
# Compiled at: 2015-03-17 17:54:10
from django import forms
from .models import *
import autocomplete_light
from django.forms.models import inlineformset_factory

class EstructuraCotizacionForm(forms.ModelForm):
    carpeta_base = forms.ModelChoiceField(queryset=Carpeta.objects.filter(carpeta_padre__nombre='/'), widget=forms.Select(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = EstructuraCotizacion


class DetalleEstructuraCotizacionForm(forms.ModelForm):
    carpeta = forms.ModelChoiceField(queryset=Carpeta.objects.all(), widget=forms.Select(attrs={'class': 'form-control hidden'}))

    class Meta:
        model = DetalleEstructuraCotizacion


def EstructuraCotizacionDetalleFormset(form, **kwargs):
    return inlineformset_factory(EstructuraCotizacion, DetalleEstructuraCotizacion, form, **kwargs)