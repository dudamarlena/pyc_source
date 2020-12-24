# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/linkexchange_django/views.py
# Compiled at: 2011-05-12 16:14:42
from django.http import Http404, HttpResponse
from linkexchange_django import support

def handle_request(request):
    if support.platform is None:
        raise Http404
    page_request = support.convert_request(request)
    page_response = support.platform.handle_request(page_request)
    if page_response.status == 404 and not page_response.body:
        raise Http404
    headers = page_response.headers.copy()
    response = HttpResponse(page_response.body, content_type=headers.pop('Content-Type', 'text/html'), status=page_response.status)
    for k, v in headers.items():
        response[k] = v

    return response