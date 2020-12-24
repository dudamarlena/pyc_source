# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\GitHub\django-microsip-base\django_microsip_base\django_microsip_base\apps\plugins\django-microsip-consolidador\django-microsip-consolidador\views.py
# Compiled at: 2015-04-21 11:28:26
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.db import connections
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from .forms import *
from microsip_api.comun.sic_db import get_conecctionname
from django.views.generic.list import ListView
import django_filters
from microsip_api.comun.sic_db import get_conecctionname, get_existencias_articulo, first_or_none

def get_existencia_sucursales_by_articulo_id(clave, connection_name, articulo_nombre=None):
    bases_datos_sucursales = DatabaseSucursal.objects.filter(empresa_conexion=connection_name)
    existencias = {}
    precios = {}
    ahorro = 0
    show_ahorro = '0'
    sucursales = {}
    if articulo_nombre:
        articulo = Articulo.objects.get(nombre=articulo_nombre)
    elif clave:
        articulo_clave = first_or_none(ArticuloClave.objects.using(connection_name).filter(clave=clave))
        articulo = articulo_clave.articulo
    if articulo:
        almacen = Almacen.objects.filter(es_predet='S')
        almacen_nombre = 'CONSOLIDADO'
        if almacen:
            almacen_nombre = almacen[0].nombre
        articulo_nombre = articulo.nombre
        existencia = get_existencias_articulo(articulo_id=articulo.id, connection_name=connection_name, fecha_inicio=datetime.now().strftime('01/01/%Y'), almacen=almacen_nombre)
        cliente_eventual = Registry.objects.get(nombre='CLIENTE_EVENTUAL_PV_ID').valor
        try:
            precio = ArticuloPrecio.objects.get(articulo=articulo, precio_empresa__id=42).precio
        except Exception as e:
            precio = 0

        precio_original = '%.2f' % precio
        descuento = articulo.get_descuento_total(cliente_id=cliente_eventual, unidades=1)
        if descuento != 0:
            precio_con_descuento = precio - precio * descuento / 100
            ahorro = '%.2f' % (precio - precio_con_descuento)
            precio_con_descuento = '%.2f' % precio_con_descuento
        else:
            precio_con_descuento = round(precio, 2)
            precio_con_descuento = '%.2f' % precio_con_descuento
        if ahorro > 0:
            show_ahorro = '1'
        sucursales['MATRIZ'] = {'existencia': existencia, 
           'precio_original': precio_original, 
           'precio_con_descuento': precio_con_descuento, 
           'descuento': descuento, 
           'ahorro': ahorro}
        for base_datos in bases_datos_sucursales:
            articulo = Articulo.objects.using(base_datos.sucursal_conexion).filter(nombre=articulo_nombre)
            almacen = Almacen.objects.using(base_datos.sucursal_conexion).filter(es_predet='S')
            almacen_nombre = 'CONSOLIDADO'
            if almacen:
                almacen_nombre = almacen[0].nombre
            if articulo.exists():
                articulo = articulo[0]
            if articulo:
                articulo_nombre = articulo.nombre
                existencia = get_existencias_articulo(articulo_id=articulo.id, connection_name=base_datos.sucursal_conexion, fecha_inicio=datetime.now().strftime('01/01/%Y'), almacen=almacen_nombre)
                cliente_eventual = Registry.objects.using(base_datos.sucursal_conexion).get(nombre='CLIENTE_EVENTUAL_PV_ID').valor
                try:
                    precio = ArticuloPrecio.objects.using(base_datos.sucursal_conexion).get(articulo=articulo, precio_empresa__id=42).precio
                except Exception as e:
                    precio

                precio_original = '%.2f' % precio
                descuento = articulo.get_descuento_total(cliente_id=cliente_eventual, unidades=1)
                if descuento != 0:
                    precio_con_descuento = precio - precio * descuento / 100
                    ahorro = '%.2f' % (precio - precio_con_descuento)
                    precio_con_descuento = '%.2f' % precio_con_descuento
                else:
                    precio_con_descuento = round(precio, 2)
                    precio_con_descuento = '%.2f' % precio_con_descuento
                if ahorro > 0:
                    show_ahorro = '1'
                sucursales[base_datos.name] = {'existencia': existencia, 'precio_original': precio_original, 
                   'precio_con_descuento': precio_con_descuento, 
                   'descuento': descuento, 
                   'ahorro': ahorro}

    return {'sucursales': sucursales, 'articulo_nombre': articulo_nombre, 'show_ahorro': show_ahorro}


@login_required(login_url='/login/')
def articulo_consolidado_view(request, clave=None, template_name='django-microsip-consolidador/articulos/articulo.html'):
    connection_name = get_conecctionname(request.session)
    form = ArticuloSearchForm(request.POST or None)
    resultado_existencias = {}
    if form.is_valid():
        clave = form.cleaned_data['clave']
        articulo = form.cleaned_data['articulo']
        articulo_nombre = None
        if articulo:
            articulo_nombre = articulo.nombre
        resultado_existencias = get_existencia_sucursales_by_articulo_id(clave=clave, connection_name=connection_name, articulo_nombre=articulo_nombre)
    if resultado_existencias != {}:
        c = {'sucursales': resultado_existencias['sucursales'], 'articulo_nombre': resultado_existencias['articulo_nombre'], 'clave': clave, 'form': form, 'show_ahorro': resultado_existencias['show_ahorro']}
    else:
        c = {'form': form}
    return render_to_response(template_name, c, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def index(request, template_name='django-microsip-consolidador/index.html'):
    return render_to_response(template_name, {}, context_instance=RequestContext(request))