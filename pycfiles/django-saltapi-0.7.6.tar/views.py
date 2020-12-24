# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/code/django-saltapi/django_saltapi/views.py
# Compiled at: 2013-03-11 15:10:33
from .control import wildcardtarget, get_salt_client, get_api_client
from .forms import LowdataForm
from .serializers import LowdataSerializer
import json
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

class JsonResponse(HttpResponse):
    """
    An HttpResponse that renders it's content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JsonResponse, self).__init__(content, **kwargs)


@wildcardtarget
def ping(request, tgt):
    client = get_salt_client()
    ret = client.cmd(tgt, 'test.ping', ret='json')
    return JsonResponse(ret)


@wildcardtarget
def echo(request, tgt, arg):
    client = get_salt_client()
    ret = client.cmd(tgt, 'test.echo', arg, ret='json')
    return JsonResponse(ret)


def minions_list(request):
    client = get_salt_client()
    ret = client.cmd('*', 'grains.items', ret='json')
    return JsonResponse(ret)


def minions_details(request, tgt):
    client = get_salt_client()
    ret = client.cmd(tgt, 'grains.items', ret='json')
    return JsonResponse(ret)


def jobs_list(request):
    client = get_api_client()
    lowdata = {'client': 'runner', 
       'fun': 'jobs.list_jobs'}
    ret = client.run(lowdata)
    return JsonResponse(ret)


def jobs_details(request, jid):
    client = get_api_client()
    lowdata = {'client': 'runner', 
       'fun': 'jobs.lookup_jid', 
       'jid': jid}
    ret = client.run(lowdata)
    return JsonResponse(ret)


@csrf_exempt
def apiwrapper(request):
    if request.method == 'POST':
        form = LowdataForm(request.POST)
        if form.is_valid():
            client = get_api_client()
            lowdata = {'client': form.cleaned_data['client'], 
               'tgt': form.cleaned_data['tgt'], 
               'fun': form.cleaned_data['fun'], 
               'arg': form.cleaned_data['arg']}
            ret = client.run(lowdata)
            return JsonResponse(ret)
        return HttpResponse(status=400)
    elif request.method == 'GET':
        return render(request, 'index.html')