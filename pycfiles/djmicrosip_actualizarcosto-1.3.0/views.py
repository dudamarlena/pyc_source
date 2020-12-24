# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\djmicrosip_actualizarcosto\djmicrosip_actualizarcosto\views.py
# Compiled at: 2017-03-17 20:25:29
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from .models import *
import csv
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.list import ListView
from .forms import *
import json, datetime
from microsip_api.comun.sic_db import first_or_none

@login_required(login_url='/login/')
def index(request, template_name='djmicrosip_actualizarcosto/index.html'):
    return render_to_response(template_name, {}, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def actualizarView(request, template_name='djmicrosip_actualizarcosto/actualizar.html'):
    form = ArticuloSearchForm(request.GET)
    c = {'form': form}
    return render_to_response(template_name, c, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def ArticuloManageView(request, id=None, template_name='djmicrosip_actualizarcosto/articulo.html'):
    if id:
        articulo = get_object_or_404(Articulo, pk=id)
    else:
        articulo = Articulo()
    form = ArticuloForm(request.POST or None, instance=articulo)
    try:
        tc = TipoCambio.objects.all().order_by('-fecha')[0].tipo_cambio
    except:
        tc = 1

    if form.is_valid():
        pr = first_or_none(ArticuloPrecio.objects.filter(articulo=articulo, precio_empresa__nombre='Precio Costo'))
        if pr:
            precio_a_insertar = form.cleaned_data['costo_ultima_compra']
            if pr.moneda.es_moneda_local == 'S':
                pr.precio = precio_a_insertar
            else:
                pr.precio = precio_a_insertar / tc
            pr.save()
        form.save()
        return HttpResponseRedirect('/actualizarcosto/actualizar/')
    else:
        c = {'form': form, 'Articulo': articulo}
        return render_to_response(template_name, c, context_instance=RequestContext(request))


def GetArticulobyClave(request):
    clave = request.GET['clave']
    articulo_id = None
    articulo_nombre = None
    articulo_clave = ArticuloClave.objects.filter(clave=clave)
    if articulo_clave:
        articulo_id = articulo_clave[0].articulo.id
        articulo_nombre = articulo_clave[0].articulo.nombre
    data = {'articulo_id': articulo_id, 
       'articulo_nombre': articulo_nombre}
    data = json.dumps(data)
    return HttpResponse(data, mimetype='application/json')