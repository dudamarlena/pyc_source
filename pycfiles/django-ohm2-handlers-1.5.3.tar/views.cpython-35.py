# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/Clients/ohm2/Entwicklung/ohm2-dev/application/website/apps/ohm2_handlers/countries/views.py
# Compiled at: 2016-12-06 12:14:58
# Size of source mod 2**32: 584 bytes
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from . import viewsdispatcher as dispatcher

def index(request):
    keys = []
    ret, error = dispatcher.view_base(request, 'GET', dispatcher.index, keys)
    if error:
        return redirect('/')
    request.context['ret'] = ret
    request.context['template'] = 'index'
    return render(request, 'countries/base_template.html', request.context)