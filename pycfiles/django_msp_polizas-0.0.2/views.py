# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SIC2-U\Documents\GitHub\django-microsip-base\django_microsip_base\apps\plugins\django_msp_polizas\django_msp_polizas\views.py
# Compiled at: 2014-10-20 16:12:45
from django.shortcuts import render_to_response
from django.template import RequestContext
from microsip_api.comun.sic_db import get_conecctionname, first_or_none
from django.contrib.auth.decorators import login_required
from .models import *
import csv
from django.http import HttpResponse
from django.views.generic.list import ListView

@login_required(login_url='/login/')
def index(request, template_name='django_msp_polizas/index.html'):
    parent = first_or_none(Registry.objects.filter(nombre='PreferenciasEmpresa'))
    if request.user.is_superuser and parent:
        if not Registry.objects.filter(nombre='SIC_polizas_cuenta_venta').exists():
            Registry.objects.create(nombre='SIC_polizas_cuenta_venta', tipo='V', padre=parent, valor='')
    return render_to_response(template_name, {}, context_instance=RequestContext(request))