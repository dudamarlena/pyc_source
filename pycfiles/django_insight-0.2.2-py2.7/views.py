# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insight/views.py
# Compiled at: 2014-09-10 07:58:57
from django.http import HttpResponseRedirect
from insight.models import Origin
from insight.signals import origin_hit

def set_origin_code(request, code):
    try:
        origin = Origin.objects.get(code=code)
        if origin.track_registrations:
            request.session['insight_code'] = code
            request.session['insight_params'] = request.GET
        origin_hit.send(sender=Origin, instance=origin, request=request)
        if origin.redirect_to:
            return HttpResponseRedirect(origin.redirect_to)
    except Origin.DoesNotExist:
        pass

    return HttpResponseRedirect('/')