# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\djmicrosip_polizas\djmicrosip_polizas\modulos\preferencias\forms.py
# Compiled at: 2016-04-13 11:53:07
from .models import *
from django import forms
import autocomplete_light

class PreferenciasManageForm(forms.Form):
    cuenta_venta = forms.ModelChoiceField(queryset=ContabilidadCuentaContable.objects.all(), widget=autocomplete_light.ChoiceWidget('ContabilidadCuentaContableAutocomplete'))
    cuenta_ventas_impuesto = forms.ModelChoiceField(queryset=ContabilidadCuentaContable.objects.all(), widget=autocomplete_light.ChoiceWidget('ContabilidadCuentaContableAutocomplete'), required=False)
    cuenta_ventas_exenta = forms.ModelChoiceField(queryset=ContabilidadCuentaContable.objects.all(), widget=autocomplete_light.ChoiceWidget('ContabilidadCuentaContableAutocomplete'), required=False)
    cuenta_clientes_venta = forms.ModelChoiceField(queryset=ContabilidadCuentaContable.objects.all(), widget=autocomplete_light.ChoiceWidget('ContabilidadCuentaContableAutocomplete'), required=False)
    cuenta_clientes_ventas_impuesto = forms.ModelChoiceField(queryset=ContabilidadCuentaContable.objects.all(), widget=autocomplete_light.ChoiceWidget('ContabilidadCuentaContableAutocomplete'), required=False)
    cuenta_clientes_ventas_exenta = forms.ModelChoiceField(queryset=ContabilidadCuentaContable.objects.all(), widget=autocomplete_light.ChoiceWidget('ContabilidadCuentaContableAutocomplete'), required=False)
    redirecionar_agruparpolizas = forms.BooleanField(required=False)

    def clean_cuenta_venta(self):
        cuenta_venta = self.cleaned_data['cuenta_venta']
        if ContabilidadCuentaContable.objects.filter(cuenta_padre=cuenta_venta.id).count() > 1:
            raise forms.ValidationError('La cuenta contabe (%s) no es de ultimo nivel. Por favor selecciona otra cuenta.' % cuenta_venta)
        return cuenta_venta

    def clean_cuenta_ventas_impuesto(self):
        cuenta_ventas_impuesto = self.cleaned_data['cuenta_ventas_impuesto']
        if cuenta_ventas_impuesto:
            if ContabilidadCuentaContable.objects.filter(cuenta_padre=cuenta_ventas_impuesto.id).count() > 1:
                raise forms.ValidationError('La cuenta contabe (%s) no es de ultimo nivel. Por favor selecciona otra cuenta.' % cuenta_ventas_impuesto)
        return cuenta_ventas_impuesto

    def clean_cuenta_ventas_exenta(self):
        cuenta_ventas_exenta = self.cleaned_data['cuenta_ventas_exenta']
        if cuenta_ventas_exenta:
            if ContabilidadCuentaContable.objects.filter(cuenta_padre=cuenta_ventas_exenta.id).count() > 1:
                raise forms.ValidationError('La cuenta contabe (%s) no es de ultimo nivel. Por favor selecciona otra cuenta.' % cuenta_ventas_exenta)
        return cuenta_ventas_exenta

    def clean_cuenta_clientes_venta(self):
        cuenta_clientes_venta = self.cleaned_data['cuenta_clientes_venta']
        if cuenta_clientes_venta:
            if ContabilidadCuentaContable.objects.filter(cuenta_padre=cuenta_clientes_venta.id).count() > 1:
                raise forms.ValidationError('La cuenta contabe (%s) no es de ultimo nivel. Por favor selecciona otra cuenta.' % cuenta_clientes_venta)
        return cuenta_clientes_venta

    def clean_cuenta_clientes_ventas_impuesto(self):
        cuenta_clientes_ventas_impuesto = self.cleaned_data['cuenta_clientes_ventas_impuesto']
        if cuenta_clientes_ventas_impuesto:
            if ContabilidadCuentaContable.objects.filter(cuenta_padre=cuenta_clientes_ventas_impuesto.id).count() > 1:
                raise forms.ValidationError('La cuenta contabe (%s) no es de ultimo nivel. Por favor selecciona otra cuenta.' % cuenta_clientes_ventas_impuesto)
        return cuenta_clientes_ventas_impuesto

    def clean_cuenta_clientes_ventas_exenta(self):
        cuenta_clientes_ventas_exenta = self.cleaned_data['cuenta_clientes_ventas_exenta']
        if cuenta_clientes_ventas_exenta:
            if ContabilidadCuentaContable.objects.filter(cuenta_padre=cuenta_clientes_ventas_exenta.id).count() > 1:
                raise forms.ValidationError('La cuenta contabe (%s) no es de ultimo nivel. Por favor selecciona otra cuenta.' % cuenta_clientes_ventas_exenta)
        return cuenta_clientes_ventas_exenta

    def save(self, *args, **kwargs):
        cuenta_venta = Registry.objects.get(nombre='SIC_polizas_cuenta_venta')
        cuenta_venta.valor = self.cleaned_data['cuenta_venta'].id
        cuenta_venta.save()
        cuenta_ventas_impuesto = Registry.objects.get(nombre='SIC_polizas_cuentaVentasImpuesto')
        if self.cleaned_data['cuenta_ventas_impuesto']:
            cuenta_ventas_impuesto.valor = self.cleaned_data['cuenta_ventas_impuesto'].id
            cuenta_ventas_impuesto.save()
        cuenta_ventas_exenta = Registry.objects.get(nombre='SIC_polizas_cuentaVentasExentas')
        if self.cleaned_data['cuenta_ventas_exenta']:
            cuenta_ventas_exenta.valor = self.cleaned_data['cuenta_ventas_exenta'].id
            cuenta_ventas_exenta.save()
        cuenta_clientes_venta = Registry.objects.get(nombre='SIC_polizas_cuentaClientes')
        cuenta_id = None
        if self.cleaned_data['cuenta_clientes_venta']:
            cuenta_id = self.cleaned_data['cuenta_clientes_venta'].id
        cuenta_clientes_venta.valor = cuenta_id
        cuenta_clientes_venta.save()
        cuenta_clientes_ventas_impuesto = Registry.objects.get(nombre='SIC_polizas_cuentaClientesVentasImpuestos')
        cuenta_id = None
        if self.cleaned_data['cuenta_clientes_ventas_impuesto']:
            cuenta_id = self.cleaned_data['cuenta_clientes_ventas_impuesto'].id
        cuenta_clientes_ventas_impuesto.valor = cuenta_id
        cuenta_clientes_ventas_impuesto.save()
        cuenta_clientes_ventas_exenta = Registry.objects.get(nombre='SIC_polizas_cuentaClientesVentasExcentas')
        cuenta_id = None
        if self.cleaned_data['cuenta_clientes_ventas_exenta']:
            cuenta_id = self.cleaned_data['cuenta_clientes_ventas_exenta'].id
        cuenta_clientes_ventas_exenta.valor = cuenta_id
        cuenta_clientes_ventas_exenta.save()
        redirecionar_agruparpolizas = Registry.objects.get(nombre='SIC_polizas_regirecionarAgrupar')
        redirecionar_agruparpolizas.valor = self.cleaned_data['redirecionar_agruparpolizas']
        redirecionar_agruparpolizas.save()
        return