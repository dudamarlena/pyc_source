# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\djmicrosip_reportes\djmicrosip_reportes\views.py
# Compiled at: 2016-06-27 12:00:17
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
import csv
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.db import connections, router

@login_required(login_url='/login/')
def index(request, template_name='djmicrosip_reportes/index.html'):
    return render_to_response(template_name, {}, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def existencia_linea(request, template_name='djmicrosip_reportes/existencia_linea.html'):
    form = lineaForm(request.POST or None)
    lista = None
    if form.is_valid():
        linea = form.cleaned_data['linea']
        using = router.db_for_write(Articulo)
        c = connections[using].cursor()
        query = "select (select first 1 clave_articulo from claves_articulos where articulo_id=ar.articulo_id) as clave, ar.nombre, ar.costo_ultima_compra, inv.inv_fin_unid\n                from articulos ar left join orsp_in_aux_art(ar.articulo_id,'Consolidado','01/01/2000',current_date, 'N','N') inv on inv.articulo_id=ar.articulo_id\n                join lineas_articulos li on li. linea_articulo_id = ar.linea_articulo_id where li.linea_articulo_id=%s\n                order by ar.nombre" % linea.id
        c.execute(query)
        lista = c.fetchall()
    c = {'form': form, 
       'lista': lista}
    return render_to_response(template_name, c, context_instance=RequestContext(request))