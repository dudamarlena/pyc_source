# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\djmicrosip_polizasautomaticas\djmicrosip_polizasautomaticas\forms.py
# Compiled at: 2018-07-04 11:50:14
from django import forms
from .models import *
import autocomplete_light
from django.conf import settings
if 'djmicrosip_tareas' in settings.EXTRA_MODULES:
    from djmicrosip_tareas.models import ProgrammedTask

    class ProgrammedTaskForm(forms.ModelForm):
        period_start_datetime = forms.CharField(label='Inicio', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fecha inicio periodo...'}))
        period_end_datetime = forms.CharField(label='Fin', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '...'}), required=False)
        period_quantity = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'unidades...'}))
        next_execution = forms.CharField(widget=forms.HiddenInput(), required=False)
        integrar_contabilidad = forms.BooleanField(required=False)
        VENTAS_TIPOS = (
         ('-', '--------------'),
         ('F', 'Facturas'),
         ('R', 'Remisiones'))
        ventas_tipodocumento = forms.ChoiceField(label='Crear Pólizas de documentos (Ventas) de', required=False, choices=VENTAS_TIPOS, widget=forms.Select(attrs={'class': 'form-control'}))
        PUNTOVENTA_TIPOS = (
         ('-', '--------------'),
         ('F', 'Facturas'),
         ('V', 'Ventas de mostrador'))
        crear_polizas_como_pendientes = forms.BooleanField(required=False)
        permitir_modificar_polizas = forms.BooleanField(required=False)
        puntodeventa_tipodocumento = forms.ChoiceField(label='Crear Pólizas de documentos (Punto de venta) de', required=False, choices=PUNTOVENTA_TIPOS, widget=forms.Select(attrs={'class': 'form-control'}))

        class Meta:
            model = ProgrammedTask
            exclude = ('description', 'command_type', 'command', 'status', 'last_execution')
            widgets = {'period_unit': forms.Select(attrs={'class': 'form-control'})}

        def save(self, *args, **kwargs):
            integrar_contabilidad_cd = self.cleaned_data['integrar_contabilidad']
            integrar_contabilidad = Registry.objects.get(nombre='SIC_POLIZAS_AUTOMATICAS_integrar_contabilidad')
            integrar_contabilidad.valor = integrar_contabilidad_cd
            integrar_contabilidad.save()
            ventas_tipodocumento_cd = self.cleaned_data['ventas_tipodocumento']
            ventas_tipodocumento = Registry.objects.get(nombre='SIC_POLIZAS_AUTOMATICAS_tipo_ve')
            ventas_tipodocumento.valor = ventas_tipodocumento_cd
            ventas_tipodocumento.save()
            crear_polizas_como_pendientes_cd = self.cleaned_data['crear_polizas_como_pendientes']
            crear_polizas_como_pendientes = Registry.objects.get(nombre='SIC_POLIZAS_AUTOMATICAS_pendientes')
            crear_polizas_como_pendientes.valor = crear_polizas_como_pendientes_cd
            crear_polizas_como_pendientes.save()
            permitir_modificar_polizas_cd = self.cleaned_data['permitir_modificar_polizas']
            permitir_modificar_polizas = Registry.objects.get(nombre='SIC_POLIZAS_AUTOMATICAS_modificar')
            permitir_modificar_polizas.valor = permitir_modificar_polizas_cd
            permitir_modificar_polizas.save()
            puntodeventa_tipodocumento_cd = self.cleaned_data['puntodeventa_tipodocumento']
            puntodeventa_tipodocumento = Registry.objects.get(nombre='SIC_POLIZAS_AUTOMATICAS_tipo_pv')
            puntodeventa_tipodocumento.valor = puntodeventa_tipodocumento_cd
            puntodeventa_tipodocumento.save()
            return super(ProgrammedTaskForm, self).save(*args, **kwargs)


class GeneraAnterioresForm(forms.Form):
    start_date = forms.CharField(label='Inicio', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Inicio'}))
    end_date = forms.CharField(label='Fin', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fin'}), required=False)


class ReemplazaCuentaForm(forms.Form):
    cuenta_iva_contado = forms.ModelChoiceField(queryset=ContabilidadCuentaContable.objects.all(), widget=autocomplete_light.ChoiceWidget('ContabilidadCuentaContableAutocomplete', attrs={'class': 'form-control'}), required=False)
    cuenta_iva_credito = forms.ModelChoiceField(queryset=ContabilidadCuentaContable.objects.all(), widget=autocomplete_light.ChoiceWidget('ContabilidadCuentaContableAutocomplete', attrs={'class': 'form-control'}), required=False)
    start_date = forms.CharField(label='Inicio', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Inicio'}))
    end_date = forms.CharField(label='Fin', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fin'}), required=False)


class SeparaVentasForm(forms.Form):
    cuenta_venta = forms.ModelChoiceField(queryset=ContabilidadCuentaContable.objects.all(), widget=autocomplete_light.ChoiceWidget('ContabilidadCuentaContableAutocomplete'))
    cuenta_ventas_impuesto = forms.ModelChoiceField(queryset=ContabilidadCuentaContable.objects.all(), widget=autocomplete_light.ChoiceWidget('ContabilidadCuentaContableAutocomplete'), required=False)
    cuenta_ventas_exenta = forms.ModelChoiceField(queryset=ContabilidadCuentaContable.objects.all(), widget=autocomplete_light.ChoiceWidget('ContabilidadCuentaContableAutocomplete'), required=False)
    start_date = forms.CharField(label='Inicio', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Inicio'}))
    end_date = forms.CharField(label='Fin', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fin'}), required=False)