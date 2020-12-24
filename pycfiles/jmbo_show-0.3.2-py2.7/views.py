# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/show/views.py
# Compiled at: 2013-09-27 03:40:37
from django.template import RequestContext
from django.shortcuts import render_to_response
from show.models import Show, RadioShow
from show.utils import get_current_permitted_show

def schedule(request):
    di = {}
    for show in Show.permitted.all():
        di.setdefault(show.repeat, [])
        di[show.repeat].append(show.id)

    for k, v in di.items():
        di[k] = Show.permitted.filter(id__in=v).order_by('start_time')

    extra = dict(intervals=di)
    return render_to_response('show/schedule.html', extra, context_instance=RequestContext(request))


def current_radio(request):
    extra = dict(object=get_current_permitted_show(RadioShow))
    return render_to_response('show/current_radio.html', extra, context_instance=RequestContext(request))