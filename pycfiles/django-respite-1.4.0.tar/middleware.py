# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jgorset/code/python/libraries/respite/respite/middleware.py
# Compiled at: 2012-11-28 12:00:07
import re
from urllib import urlencode
from django.http import QueryDict
from django.utils import simplejson as json
from respite.utils import parse_content_type, parse_multipart_data
from respite.utils.datastructures import NestedQueryDict

class HttpMethodOverrideMiddleware:
    """
    Facilitate for overriding the HTTP method with the X-HTTP-Method-Override
    header or a '_method' HTTP POST parameter.
    """

    def process_request(self, request):
        request._raw_post_data = re.sub('_method=(GET|POST|PUT|PATCH|DELETE|OPTIONS)&?', '', request.raw_post_data)
        if 'HTTP_X_HTTP_METHOD_OVERRIDE' in request.META or '_method' in request.POST:
            request.method = (request.META.get('HTTP_X_HTTP_METHOD_OVERRIDE') or request.POST.get('_method')).upper()
            if 'csrfmiddlewaretoken' in request.POST:
                request.META.setdefault('HTTP_X_CSRFTOKEN', request.POST['csrfmiddlewaretoken'])
            request.POST = QueryDict('')


class HttpPutMiddleware:
    """
    Facilitate for HTTP PUT in the same way Django facilitates for HTTP GET
    and HTTP POST; populate a QueryDict instance with the request body in request.PUT.
    """

    def process_request(self, request):
        if request.method == 'PUT':
            if request.META.get('CONTENT_TYPE', '').startswith('multipart'):
                request.PUT = parse_multipart_data(request)[0]
            else:
                request.PUT = QueryDict(request.raw_post_data)


class HttpPatchMiddleware:
    """
    Facilitate for HTTP PATCH in the same way Django facilitates for HTTP GET
    and HTTP POST; populate a QueryDict instance with the request body in request.PATCH.
    """

    def process_request(self, request):
        if request.method == 'PATCH':
            if request.META.get('CONTENT_TYPE', '').startswith('multipart'):
                request.PATCH = parse_multipart_data(request)[0]
            else:
                request.PATCH = QueryDict(request.raw_post_data)


class JsonMiddleware:
    """
    Parse JSON in POST, PUT and PATCH requests.
    """

    def process_request(self, request):
        if 'CONTENT_TYPE' in request.META:
            content_type, encoding = parse_content_type(request.META['CONTENT_TYPE'])
            if content_type == 'application/json':
                data = json.loads(request.raw_post_data, encoding)
                if request.method in ('POST', 'PUT', 'PATCH'):
                    setattr(request, request.method, NestedQueryDict(data))