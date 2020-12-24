# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SIC2-U\Documents\GitHub\django-microsip-base\django_microsip_base\apps\plugins\django_msp_polizas\django_msp_polizas\modulos\preferencias\forms.py
# Compiled at: 2014-10-20 22:24:03
from .models import *
from django import forms
import autocomplete_light

class PreferenciasManageForm(forms.Form):
    cuenta_venta = forms.ModelChoiceField(queryset=ContabilidadCuentaContable.objects.all(), widget=autocomplete_light.ChoiceWidget('ContabilidadCuentaContableAutocomplete'))

    def clean_cuenta_venta(self):
        cuenta_venta = self.cleaned_data['cuenta_venta']
        if ContabilidadCuentaContable.objects.filter(cuenta_padre=cuenta_venta.id).count() > 1:
            raise forms.ValidationError('La cuenta contabe (%s) no es de ultimo nivel. Por favor selecciona otra cuenta.' % cuenta_venta)
        return cuenta_venta

    def save(self, *args, **kwargs):
        cuenta_venta = Registry.objects.get(nombre='SIC_polizas_cuenta_venta')
        cuenta_venta.valor = self.cleaned_data['cuenta_venta'].id
        cuenta_venta.save()