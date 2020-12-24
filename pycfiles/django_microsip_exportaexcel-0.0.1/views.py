# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Jesus\Documents\GitHub\django-microsip-base\django_microsip_base\django_microsip_base\apps\plugins\django_microsip_exportaexcel\django_microsip_exportaexcel\views.py
# Compiled at: 2014-12-31 15:31:08
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from .models import *
import csv
from django.http import HttpResponse
from django.views.generic.list import ListView

@login_required(login_url='/login/')
def index(request, template_name='django_microsip_exportaexcel/index.html'):
    return render_to_response(template_name, {}, context_instance=RequestContext(request))