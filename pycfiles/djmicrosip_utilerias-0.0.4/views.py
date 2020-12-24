# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\GitHub\django-microsip-base\django_microsip_base\django_microsip_base\apps\plugins\djmicrosip_utilerias\djmicrosip_utilerias\views.py
# Compiled at: 2015-03-07 13:25:42
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
import csv
from django.http import HttpResponse
from django.views.generic.list import ListView
from microsip_api.comun.sic_db import first_or_none
from decimal import Decimal
from django.contrib.auth import authenticate
import json
from django.http import HttpResponseRedirect
import unicodecsv

@login_required(login_url='/login/')
def index(request, template_name='djmicrosip_utilerias/index.html'):
    return render_to_response(template_name, {}, context_instance=RequestContext(request))


def GetTipoCambio(moneda):
    tipos_cambio = first_or_none(TipoCambio.objects.filter(moneda=moneda).order_by('-fecha'))
    if tipos_cambio:
        return tipos_cambio.tipo_cambio
    return 0


def get_articulos_ids(request):
    sysdba_password = request.GET['sysdba_password']
    usuario = authenticate(username='SYSDBA', password=sysdba_password)
    error = None
    articulos_ids = []
    if not usuario:
        error = 'contraseña invalida'
    else:
        articulos_ids = Articulo.objects.all().values_list('id', flat=True)
    data = {'error': error, 
       'articulos_ids': list(articulos_ids)}
    return HttpResponse(json.dumps(data), mimetype='application/json')


def actualiza_margenes_ajax(request):
    articulos_ids = request.GET.getlist('articulos_ids')[0].split(',')
    moneda_local = Moneda.objects.get(es_moneda_local='S')
    for articulo_id in articulos_ids:
        articulo = Articulo.objects.get(id=articulo_id)
        articulos_precios = ArticuloPrecio.objects.filter(articulo=articulo)
        ultimo_costo_mn = articulo.costo_ultima_compra
        for articulo_precio in articulos_precios:
            if articulo_precio.moneda.es_moneda_local == 'S':
                ultimo_costo = ultimo_costo_mn
            else:
                tipo_cambio = GetTipoCambio(articulo_precio.moneda)
                ultimo_costo = ultimo_costo_mn / tipo_cambio
            margen = 0
            if ultimo_costo > 0:
                margen = (articulo_precio.precio / ultimo_costo - 1) * 100
                margen = Decimal(str(margen)).quantize(Decimal('.000001'))
                if margen < 0:
                    margen = 0
                elif margen > 999:
                    margen = 999
                print str(margen) + 'articulo =' + articulo_id
            if articulo_id == 52309:
                objects.asdsd
            articulo_precio.margen = margen
            articulo_precio.save(update_fields=['margen'])

    data = {}
    return HttpResponse(json.dumps(data), mimetype='application/json')


@login_required(login_url='/login/')
def actualiza_margenes_view(request, template_name='djmicrosip_utilerias/actualiza_margenes.html'):
    c = {}
    return render_to_response(template_name, c, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def exportar_precios(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="precios.csv"'
    writer = unicodecsv.writer(response, encoding='utf-8')
    articulos = Articulo.objects.all()
    for articulo in articulos:
        articulo_clave = first_or_none(ArticuloClave.objects.filter(articulo=articulo))
        if articulo_clave:
            precio = 0
            margen = 0
            clave = unicode(articulo_clave.clave).encode('utf-8')
            articulos_precios = ArticuloPrecio.objects.filter(articulo=articulo, precio_empresa__nombre='Precio de lista')
            for articulo_precio in articulos_precios:
                if articulo_precio:
                    precio = articulo_precio.precio
                    margen = articulo_precio.margen
                    lista_precio_nombre = unicode(articulo_precio.precio_empresa.nombre).encode('utf-8')
                writer.writerow((clave, lista_precio_nombre, precio, margen))

    return response


@login_required(login_url='/login/')
def importar_precios(request):
    f = open('C:\\precios.csv')
    r = unicodecsv.reader(f, encoding='utf-8')
    for row in r:
        clave = row[0]
        lista_precios_nombre = row[1]
        precio = row[2]
        margen = row[3]
        articulo_clave = first_or_none(ArticuloClave.objects.filter(clave=clave))
        if articulo_clave:
            articulo = articulo_clave.articulo
            articulo_precio = first_or_none(ArticuloPrecio.objects.filter(articulo=articulo, precio_empresa__nombre=lista_precios_nombre))
            if articulo_precio:
                articulo_precio.precio = Decimal(precio)
                articulo_precio.margen = Decimal(margen)
                articulo_precio.save(update_fields=('precio', 'margen'))

    return HttpResponseRedirect('/utilerias/')