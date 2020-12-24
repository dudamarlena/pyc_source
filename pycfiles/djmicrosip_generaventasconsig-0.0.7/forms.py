# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\GitHub\django-microsip-base\django_microsip_base\django_microsip_base\apps\plugins\djmicrosip_generaventasconsig\djmicrosip_generaventasconsig\forms.py
# Compiled at: 2015-02-16 16:52:09
from django import forms
from .models import *
from datetime import datetime
from microsip_api.comun.sic_db import first_or_none
from django.conf import settings
import autocomplete_light

class PreferenciasManageForm(forms.Form):
    busqueda_fecha_inicio = forms.DateField()
    ventas_cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), widget=autocomplete_light.ChoiceWidget('ClienteAutocomplete'))
    ventas_cajero = forms.ModelChoiceField(queryset=Cajero.objects.all())
    ventas_caja = forms.ModelChoiceField(queryset=Caja.objects.all())
    ventas_vendedor = forms.ModelChoiceField(queryset=Vendedor.objects.all())
    incremento_precio = forms.DecimalField(min_value=0, max_value=100)

    def __init__(self, *args, **kwargs):
        bases_de_datos = settings.MICROSIP_DATABASES.keys()
        empresas = []
        for database_conexion in bases_de_datos:
            try:
                database_conexion = '%s' % database_conexion
            except UnicodeDecodeError:
                pass
            else:
                conexion_id, empresa = database_conexion.split('-')
                conexion = ConexionDB.objects.get(pk=int(conexion_id))
                database_conexion_name = '%s-%s' % (conexion.nombre, empresa)
                empresa_option = [
                 database_conexion, database_conexion_name]
                empresas.append(empresa_option)

        super(PreferenciasManageForm, self).__init__(*args, **kwargs)
        self.fields['busqueda_database'] = forms.ChoiceField(choices=empresas)
        self.fields['busqueda_database'].widget.attrs['class'] = 'form-control'
        self.fields['ventas_cajero'].widget.attrs['class'] = 'form-control'
        self.fields['ventas_caja'].widget.attrs['class'] = 'form-control'
        self.fields['ventas_vendedor'].widget.attrs['class'] = 'form-control'
        self.fields['incremento_precio'].widget.attrs['class'] = 'form-control'

    def save(self, *args, **kwargs):
        registry = Registry.objects.get(nombre='SIC_generaVentasConsig_fechaInicio')
        registry.valor = self.cleaned_data['busqueda_fecha_inicio']
        registry.save(update_fields=('valor', ))
        registry = Registry.objects.get(nombre='SIC_generaVentasConsig_empresa')
        registry.valor = self.cleaned_data['busqueda_database']
        registry.save(update_fields=('valor', ))
        registry = Registry.objects.get(nombre='SIC_generaVentasConsig_cliente')
        registry.valor = self.cleaned_data['ventas_cliente']
        registry.save(update_fields=('valor', ))
        registry = Registry.objects.get(nombre='SIC_generaVentasConsig_cajero')
        registry.valor = self.cleaned_data['ventas_cajero']
        registry.save(update_fields=('valor', ))
        registry = Registry.objects.get(nombre='SIC_generaVentasConsig_caja')
        registry.valor = self.cleaned_data['ventas_caja']
        registry.save(update_fields=('valor', ))
        registry = Registry.objects.get(nombre='SIC_generaVentasConsig_vendedor')
        registry.valor = self.cleaned_data['ventas_vendedor']
        registry.save(update_fields=('valor', ))
        registry = Registry.objects.get(nombre='SIC_generaVentasConsig_incrementoPrecio')
        registry.valor = self.cleaned_data['incremento_precio']
        registry.save(update_fields=('valor', ))