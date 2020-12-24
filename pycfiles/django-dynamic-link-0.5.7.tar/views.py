# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stein/Projekte/eclipse/django-dynamic-link/dynamicLink/views.py
# Compiled at: 2013-04-23 04:56:27
__author__ = 'Andreas Fritz - sources.e-blue.eu'
__copyright__ = 'Copyright (c) ' + '28.08.2010' + ' Andreas Fritz'
__licence__ = 'New BSD Licence'
import os, presettings
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render_to_response
from django.template import RequestContext
import mimetypes
from django.views.decorators.cache import cache_control
from django.utils.translation import ugettext_lazy as _
from models import Download, IsExpiredError

def expired(key):
    expired_objects = Download.objects.filter(active=False)
    for obj in expired_objects:
        if key == obj.link_key:
            return obj


def active(key):
    active_objects = Download.objects.filter(active=True)
    for obj in active_objects:
        if key == obj.link_key:
            return obj


def error(request, text=_('Sorry, your request is not available')):
    """returns the error page"""
    extra_context = {'message': text}
    template = 'dynamicLink/not_avallible.html'
    return render_to_response(template, extra_context, context_instance=RequestContext(request))


def site(request, offset):
    """process site requests"""
    offset = offset.split('-')
    obj = {'actives': [], 'expired': [], 'notexist': []}
    for key in offset:
        if active(key):
            obj['actives'].append(active(key))
        elif expired(key):
            obj['expired'].append(expired(key))
        else:
            obj['notexist'].append(key)

    template = 'dynamicLink/provide.html'
    extra_context = {'basepath': presettings.DYNAMIC_LINK_URL_BASE_COMPONENT, 
       'downloads': obj}
    return render_to_response(template, extra_context, context_instance=RequestContext(request))


def fetch(request, offset):
    """process link requests. make desissions for every single download link"""
    if active(offset):
        return provide(request, offset)
    else:
        if expired(offset):
            return error(request, presettings.TEXT_REQUEST_IS_EXPIRED)
        return error(request, presettings.TEXT_REQUEST_DOES_NOT_EXIST)


@cache_control(private=True)
def provide(request, key):
    """
    Return a download without the rael path to the served file.
    The content will served by a stream.

    The file will read in byte code to a socket wich will be
    used in the response object. Headers in the response will
    set for the specific served content referable to its type.
    """
    stored_file_obj = Download.objects.get(link_key=key)
    try:
        filepath = stored_file_obj.get_path()
    except IsExpiredError:
        return error(request)

    delimiter = presettings.DYNAMIC_LINK_MEDIA.strip('/').split('/')[(-1)]
    file_path = os.path.normpath(presettings.DYNAMIC_LINK_MEDIA + '/' + filepath.split(delimiter)[(-1)])
    try:
        fsocket = open(file_path, 'rb')
    except IOError:
        stored_file_obj.active = False
        stored_file_obj.save()
        return HttpResponseNotFound(unicode(_('File not found!')))

    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    auto_mimetype, auto_encoding = mimetypes.guess_type(file_path)
    if not auto_mimetype:
        auto_mimetype = 'application/octet-stream'
    response = HttpResponse(fsocket, mimetype=auto_mimetype)
    response['Content-Disposition'] = 'attachment; filename=%s' % file_name.encode('utf-8')
    if auto_encoding and auto_encoding is not 'gzip':
        response['Content-Encoding'] = auto_encoding
    response['Content-Length'] = file_size
    return response