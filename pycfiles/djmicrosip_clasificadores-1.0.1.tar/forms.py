# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\djmicrosip_apps\djmicrosip_clasificadores\djmicrosip_clasificadores\forms.py
# Compiled at: 2020-04-27 13:10:50
from django import forms
import fdb, os
from datetime import date
from django.forms.models import inlineformset_factory
import autocomplete_light
from django.db import router, connections, connection
from django.contrib.sites.models import Site
from .models import *
from microsip_api.models_base.models import ConexionDB, DatabaseSucursal
from django_microsip_base.libs.models_base.models import Articulo, ArticuloPrecio, ArticuloClave, Clasificadores, ClasificadoresValores, ElementosClasificadores, GrupoLineas, LineaArticulos, Cliente, Registry, Cajero, Caja

class FilterForm(forms.Form):
    busqueda = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'place-holder': 'Ingrese criterio de busqueda'}), required=False)
    sin_existencia = forms.BooleanField(required=False)


class PreferenciasManageForm(forms.Form):

    def __init__(self, *args, **kwargs):
        empresas = []
        conexion_activa = kwargs.pop('conexion_activa')
        if conexion_activa != '':
            conexion_activa = ConexionDB.objects.get(pk=conexion_activa)
        else:
            conexion_activa = None
        if conexion_activa:
            db = fdb.connect(host=conexion_activa.servidor, user=conexion_activa.usuario, password=conexion_activa.password, database='%s\\System\\CONFIG.FDB' % conexion_activa.carpeta_datos)
            c = db.cursor()
            query = 'SELECT EMPRESAS.nombre_corto FROM EMPRESAS order by nombre_corto'
            c.execute(query)
            empresas_rows = c.fetchall()
            for empresa in empresas_rows:
                try:
                    empresa = '%s' % empresa[0]
                except UnicodeDecodeError:
                    pass
                else:
                    empresa_option = [
                     empresa, empresa]
                    empresas.append(empresa_option)

        super(PreferenciasManageForm, self).__init__(*args, **kwargs)
        self.fields['base_datos_automatica'] = forms.ChoiceField(choices=empresas, widget=forms.Select(attrs={'class': 'form-control'}))
        self.fields['cliente'] = forms.ModelChoiceField(queryset=Cliente.objects.all().order_by('nombre'), widget=autocomplete_light.ChoiceWidget('ClienteAutocomplete'))
        self.fields['tiempo_espera'] = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
        self.fields['clasificador_padre'] = forms.ModelChoiceField(queryset=Clasificadores.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), required=False)
        self.fields['cajero'] = forms.ModelChoiceField(queryset=Cajero.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), required=False)
        self.fields['caja'] = forms.ModelChoiceField(queryset=Caja.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), required=False)
        self.fields['limite_existencia'] = forms.BooleanField(required=False)
        MODULO = (
         ('V', 'Ventas'),
         ('PV', 'Punto de venta'))
        self.fields['modulo'] = forms.ChoiceField(choices=MODULO, widget=forms.Select(attrs={'class': 'form-control'}), required=False)
        TIPO_DOCUMENTO = (
         ('', '-------------'),
         ('C', 'Cotizacion'),
         ('P', 'Pedido'),
         ('R', 'Remision'))
        self.fields['tipo_documento'] = forms.ChoiceField(choices=TIPO_DOCUMENTO, widget=forms.Select(attrs={'class': 'form-control'}), required=False)
        self.fields['email'] = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
        self.fields['password'] = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
        self.fields['servidor_correo'] = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
        self.fields['puerto'] = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
        return

    def save(self, *args, **kwargs):
        cliente = Registry.objects.get(nombre='SIC_Clasificadores_Cliente_predeterminado')
        cliente.valor = self.cleaned_data['cliente'].id
        cliente.save()
        tiempo_espera = Registry.objects.get(nombre='SIC_Clasificadores_Tiempo_Espera')
        tiempo_espera.valor = self.cleaned_data['tiempo_espera']
        tiempo_espera.save()
        clasificador_padre = Registry.objects.get(nombre='SIC_Clasificadores_Clasificador_Padre')
        clasificador_padre.valor = self.cleaned_data['clasificador_padre'].clasificador_id
        clasificador_padre.save()
        cajero = Registry.objects.get(nombre='SIC_Clasificadores_Cajero')
        cajero.valor = self.cleaned_data['cajero'].id
        cajero.save()
        caja = Registry.objects.get(nombre='SIC_Clasificadores_Caja')
        caja.valor = self.cleaned_data['caja'].id
        caja.save()
        limite_existencia = Registry.objects.get(nombre='SIC_Clasificadores_LimiteExistencia')
        print limite_existencia
        print self.cleaned_data['limite_existencia']
        limite_existencia.valor = self.cleaned_data['limite_existencia']
        limite_existencia.save()
        modulo = Registry.objects.get(nombre='SIC_Clasificadores_Modulo')
        modulo.valor = self.cleaned_data['modulo']
        modulo.save()
        tipo_documento = Registry.objects.get(nombre='SIC_Clasificadores_Tipo_Documento')
        tipo_documento.valor = self.cleaned_data['tipo_documento']
        tipo_documento.save()
        base_datos_automatica = Registry.objects.get(nombre='SIC_Clasificadores_BD_Automatica')
        base_datos_automatica.valor = self.cleaned_data['base_datos_automatica']
        base_datos_automatica.save()
        email = Registry.objects.get(nombre='SIC_Clasificadores_Email')
        email.valor = self.cleaned_data['email']
        email.save()
        password = Registry.objects.get(nombre='SIC_Clasificadores_Password')
        password.valor = self.cleaned_data['password']
        password.save()
        servidor_correo = Registry.objects.get(nombre='SIC_Clasificadores_Servidro_Correo')
        servidor_correo.valor = self.cleaned_data['servidor_correo']
        servidor_correo.save()
        puerto = Registry.objects.get(nombre='SIC_Clasificadores_Puerto')
        puerto.valor = self.cleaned_data['puerto']
        puerto.save()
        DatabaseSucursal.objects.get_or_create(name='clasificadores', empresa_conexion=base_datos_automatica.valor)
        DatabaseSucursal.objects.get_or_create(name='SIC_Clasificadores_Email', empresa_conexion=email.valor)
        DatabaseSucursal.objects.get_or_create(name='SIC_Clasificadores_Password', empresa_conexion=password.valor)
        DatabaseSucursal.objects.get_or_create(name='SIC_Clasificadores_Servidro_Correo', empresa_conexion=servidor_correo.valor)
        DatabaseSucursal.objects.get_or_create(name='SIC_Clasificadores_Puerto', empresa_conexion=puerto.valor)


class ArticuloFindForm(forms.Form):
    nombre = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'place-holder': 'Ingrese criterio de busqueda'}), required=False)
    grupo = forms.ModelChoiceField(queryset=GrupoLineas.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    linea = forms.ModelChoiceField(queryset=LineaArticulos.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), required=False)


class UsuarioForm(forms.Form):
    usuario = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'place-holder': 'Ingrese criterio de busqueda'}), required=False)
    anterior_contrasena = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    nueva_contrasena = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'}))