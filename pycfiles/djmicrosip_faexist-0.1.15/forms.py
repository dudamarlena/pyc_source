# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Jesus\Documents\GitHub\django-microsip-base\django_microsip_base\django_microsip_base\apps\plugins\djmicrosip_faexist\djmicrosip_faexist\forms.py
# Compiled at: 2015-01-29 13:14:31
from django import forms
import autocomplete_light
from .models import *
import autocomplete_light
from datetime import datetime
from microsip_api.comun.sic_db import first_or_none
from django.conf import settings

class ArticuloSearchForm(forms.Form):
    articulo = forms.ModelChoiceField(queryset=Articulo.objects.all(), widget=autocomplete_light.ChoiceWidget('ArticuloAutocomplete'), required=False)
    linea = forms.ModelChoiceField(queryset=LineaArticulos.objects.all(), widget=autocomplete_light.ChoiceWidget('LineaArticulosAutocomplete'), required=False)
    nombre = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'nombre...'}), required=False)
    clave = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'clave...'}), required=False)
    IGNORAR_TIPOS = (
     ('T', 'Todos'),
     ('I', 'Ignorados'),
     ('SI', 'Sin Ignorar'))
    mostrar_articulos = forms.ChoiceField(choices=IGNORAR_TIPOS, widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(ArticuloSearchForm, self).__init__(*args, **kwargs)
        self.fields['articulo'].widget.attrs['class'] = 'form-control'


class PuntoVentaDocumentoForm(forms.ModelForm):
    cliente = forms.ModelChoiceField(Cliente.objects.all(), widget=autocomplete_light.ChoiceWidget('ClienteAutocomplete'), required=True)
    linea = forms.ModelChoiceField(LineaArticulos.objects.all(), widget=autocomplete_light.ChoiceWidget('LineaArticulosAutocomplete'), required=True)

    class Meta:
        model = PuntoVentaDocumento
        fields = ['cliente']


class PreferenciasManageForm(forms.Form):
    periodo_fecha_inicio = forms.DateField()
    proveedor = forms.IntegerField(widget=forms.HiddenInput())
    almacen = forms.IntegerField(widget=forms.HiddenInput())
    ventas_caja = forms.ModelChoiceField(queryset=Caja.objects.all(), required=True)
    ventas_cajero = forms.ModelChoiceField(queryset=Cajero.objects.all(), required=True)
    ventas_vendedor = forms.ModelChoiceField(queryset=Vendedor.objects.all(), required=True)
    cliente = forms.ModelChoiceField(Cliente.objects.all(), widget=autocomplete_light.ChoiceWidget('ClienteAutocomplete'), required=True)
    margen_precio_lista = forms.DecimalField(max_value=100, min_value=0, max_digits=3)
    margen_precio_costo = forms.DecimalField(max_value=100, min_value=0, max_digits=3)

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
        self.fields['database'] = forms.ChoiceField(choices=empresas)