# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/adagios/adagios/../adagios/views.py
# Compiled at: 2018-05-16 10:07:32
from django.http import HttpResponse
import traceback
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext, loader
from django import template
from django.utils.translation import ugettext as _
import time, logging, adagios.settings, adagios.utils
from adagios.exceptions import AccessDenied

def adagios_decorator(view_func):
    """ This is a python decorator intented for all views in the status module.

     It catches all unhandled exceptions and displays them on a generic web page.

     Kind of what the django exception page does when debug mode is on.
    """

    def wrapper(request, *args, **kwargs):
        start_time = time.time()
        try:
            if request.method == 'POST':
                adagios.utils.update_eventhandlers(request)
            result = view_func(request, *args, **kwargs)
            end_time = time.time()
            time_now = time.ctime()
            duration = end_time - start_time
            return result
        except Exception as e:
            c = {}
            c['exception'] = str(e)
            c['exception_type'] = str(type(e).__name__)
            c['traceback'] = traceback.format_exc()
            return error_page(request, context=c)

    wrapper.__name__ = view_func.__name__
    wrapper.__module__ = view_func.__module__
    return wrapper


def error_page(request, context=None):
    if context is None:
        context = {}
        context['errors'] = []
        context['errors'].append('Error occured, but no error messages provided, what happened?')
    if request.META.get('CONTENT_TYPE') == 'application/json':
        context.pop('request', None)
        content = str(context)
        response = HttpResponse(content=content, content_type='application/json')
    else:
        response = render_to_response('status_error.html', context, context_instance=RequestContext(request))
    response.status_code = 500
    return response


def index(request):
    """ This view is our frontpage """
    if adagios.settings.enable_status_view:
        return redirect('adagios.status.views.status_index', permanent=True)
    else:
        return redirect('objectbrowser', permanent=True)


def http_403(request, exception=None):
    context = {}
    context['exception'] = exception
    if request.META.get('CONTENT_TYPE') == 'application/json':
        c = {}
        c['exception_type'] = exception.__class__
        c['message'] = str(exception.message)
        c['access_required'] = exception.access_required
        response = HttpResponse(content=str(c), content_type='application/json')
    else:
        response = render_to_response('403.html', context, context_instance=RequestContext(request))
    response.status_code = 403
    return response