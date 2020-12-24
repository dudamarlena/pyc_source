# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\django-microsip-base\django_microsip_base\django_microsip_base\apps\main\views.py
# Compiled at: 2019-09-09 14:23:53
from django.shortcuts import render_to_response
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth.decorators import login_required
from microsip_api.comun.sic_db import get_conecctionname, get_existencias_articulo

@login_required(login_url='/login/')
def index(request):
    return render_to_response('main/index.html', {}, context_instance=RequestContext(request))