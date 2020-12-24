# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/alexandria/sessions/db/views.py
# Compiled at: 2010-10-04 19:19:47
from alexandria.sessions.db.models import *
from django.shortcuts import render_to_response
from django.utils import simplejson
from django.http import HttpResponse

def _get_data():
    data = {}
    for item in Item.objects.filter(key__in=['name', 'phone', 'technology', 'useful']):
        question_container = data.setdefault(item.key, {})
        question_container.setdefault(item.value, 0)
        question_container[item.value] += 1

    return data


def home(request):
    json = simplejson.dumps(_get_data())
    return render_to_response('home.html', locals())


def json(request):
    json = simplejson.dumps(_get_data())
    return HttpResponse(json, content_type='application/javascript')