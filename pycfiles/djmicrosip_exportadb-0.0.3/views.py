# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Jesus\Documents\GitHub\django-microsip-base\django_microsip_base\django_microsip_base\apps\plugins\djmicrosip_exportadb\djmicrosip_exportadb\views.py
# Compiled at: 2015-01-22 13:04:56
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from .models import *
import csv
from django.http import HttpResponse
from django.views.generic.list import ListView
from microsip_api.comun.sic_db import first_or_none
from .new_database_info import NEW_DB

@login_required(login_url='/login/')
def index(request, template_name='djmicrosip_exportadb/index.html'):
    clientes = Cliente.objects.filter(estatus='A')
    existe = 0
    no_existe = 0
    for cliente in clientes:
        libres_clientes = first_or_none(LibresClientes.objects.filter(id=cliente.id))
        if libres_clientes:
            cliente_nueva = first_or_none(Cliente.objects.using(NEW_DB).filter(nombre=cliente.nombre))
            if cliente_nueva:
                libres_clientes_nueva = first_or_none(LibresClientes.objects.using(NEW_DB).filter(id=cliente_nueva.id))
                if not libres_clientes_nueva:
                    LibresClientes.objects.using(NEW_DB).create(id=cliente_nueva.id, cuenta_1=libres_clientes.cuenta_1, cuenta_2=libres_clientes.cuenta_2)

    return render_to_response(template_name, {}, context_instance=RequestContext(request))