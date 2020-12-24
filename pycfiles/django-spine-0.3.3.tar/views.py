# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ikeda/.virtualenvs/rsyslog-monitor/django_spine/django-spine/examples/django_spine/spineapp/views.py
# Compiled at: 2012-07-31 11:51:14
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.http import require_POST, require_safe
from spine.utils import JsonResponse, json
from .models import Example, ExampleMapper

def index(request):
    if request.method == 'GET':
        if request.is_ajax():
            return JsonResponse(map(lambda obj: ExampleMapper(obj).as_dict(), Example.objects.all()))
        else:
            return render_to_response('spineapp/app.html', RequestContext(request, {}))

    try:
        data = json.loads(request.body)
        data.pop('id')
        post = Example(**data)
        post.save()
        return JsonResponse(ExampleMapper(post).as_dict())
    except Exception as err:
        return JsonResponse({'err': err.message})


@require_POST
def show(request):
    pass


@require_safe
def new(request):
    pass


@require_safe
def edit(request):
    pass


@require_POST
def update(request):
    pass


@require_POST
def destroy(request):
    pass