# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\djmicrosip_polizas\djmicrosip_polizas\views.py
# Compiled at: 2016-04-13 11:53:07
from django.shortcuts import render_to_response
from django.template import RequestContext
from microsip_api.comun.sic_db import get_conecctionname, first_or_none
from django.contrib.auth.decorators import login_required
from .models import *
import csv
from django.http import HttpResponse
from django.views.generic.list import ListView

@login_required(login_url='/login/')
def index(request, template_name='djmicrosip_polizas/index.html'):
    return render_to_response(template_name, {}, context_instance=RequestContext(request))