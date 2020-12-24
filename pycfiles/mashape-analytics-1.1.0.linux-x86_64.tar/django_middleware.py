# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/.virtualenvs/mashape-test/lib/python2.7/site-packages/mashapeanalytics/middleware/django_middleware.py
# Compiled at: 2016-05-17 13:24:26
from __future__ import unicode_literals
import re, socket
from datetime import datetime
from django.conf import settings
from six.moves import cStringIO
from six.moves.urllib.parse import parse_qs
from mashapeanalytics.transport import HttpTransport
from mashapeanalytics.alf import Alf
from werkzeug.wrappers import Request

class DjangoMiddleware(object):

    def __init__(self):
        self.serviceToken = getattr(settings, b'MASHAPE_ANALYTICS_SERVICE_TOKEN', None)
        self.environment = getattr(settings, b'MASHAPE_ANALYTICS_ENVIRONMENT', None)
        host = getattr(settings, b'MASHAPE_ANALYTICS_HOST', b'collector.galileo.mashape.com')
        port = int(getattr(settings, b'MASHAPE_ANALYTICS_PORT', 443))
        connection_timeout = int(getattr(settings, b'MASHAPE_ANALYTICS_CONNECTION_TIMEOUT', 30))
        retry_count = int(getattr(settings, b'MASHAPE_ANALYTICS_RETRY_COUNT', 0))
        self.transport = HttpTransport(host, port, connection_timeout, retry_count)
        if self.serviceToken is None:
            raise AttributeError(b"'MASHAPE_ANALYTICS_SERVICE_TOKEN' setting is not found.")
        return

    def process_request(self, request):
        request.META[b'MASHAPE_ANALYTICS.STARTED_DATETIME'] = datetime.utcnow()
        request.META[b'galileo.request'] = Request(request.META)

    def request_header_size(self, request):
        first_line = len(request.META.get(b'REQUEST_METHOD')) + len(request.get_full_path()) + 12
        header_fields = sum([ len(header) + len(value) - 1 for header, value in request.META.items() if header.startswith(b'HTTP_') ])
        last_line = 2
        return first_line + header_fields + last_line

    def client_address(self, request):
        ip = request.META.get(b'HTTP_X_FORWARDED_FOR', request.META.get(b'REMOTE_ADDR', None))
        if ip:
            return ip.split(b',')[0]
        else:
            return

    def response_header_size(self, response):
        first_line = len(str(response.status_code)) + len(response.reason_phrase) + 10
        header_fields = sum([ len(header) + len(value) + 4 for header, value in response._headers.items() ])
        return first_line + header_fields

    def process_response(self, request, response):
        startedDateTime = request.META.get(b'MASHAPE_ANALYTICS.STARTED_DATETIME', datetime.utcnow())
        requestHeaders = [ {b'name': re.sub(b'^HTTP_', b'', header), b'value': value} for header, value in request.META.items() if header.startswith(b'HTTP_') ]
        requestHeaderSize = self.request_header_size(request)
        requestQueryString = [ {b'name': name, b'value': value[0] if len(value) > 0 else None} for name, value in parse_qs(request.META.get(b'QUERY_STRING', b'')).items() ]
        r = request.META.get(b'galileo.request')
        requestContentSize = r.content_length or 0
        responseHeaders = [ {b'name': header, b'value': value[(-1)]} for header, value in response._headers.items() ]
        responseHeadersSize = self.response_header_size(response)
        responseContentSize = len(response.content)
        alf = Alf(self.serviceToken, self.environment, self.client_address(request))
        alf.addEntry({b'startedDateTime': startedDateTime.isoformat() + b'Z', 
           b'serverIpAddress': socket.gethostbyname(socket.gethostname()), 
           b'time': int(round((datetime.utcnow() - startedDateTime).total_seconds() * 1000)), 
           b'request': {b'method': request.method, 
                        b'url': request.build_absolute_uri(), 
                        b'httpVersion': b'HTTP/1.1', 
                        b'cookies': [], b'queryString': requestQueryString, 
                        b'headers': requestHeaders, 
                        b'headersSize': requestHeaderSize, 
                        b'content': {b'size': requestContentSize, 
                                     b'mimeType': request.META.get(b'CONTENT_TYPE', b'application/octet-stream')}, 
                        b'bodySize': requestContentSize}, 
           b'response': {b'status': response.status_code, 
                         b'statusText': response.reason_phrase, 
                         b'httpVersion': b'HTTP/1.1', 
                         b'cookies': [], b'headers': responseHeaders, 
                         b'headersSize': responseHeadersSize, 
                         b'content': {b'size': responseContentSize, 
                                      b'mimeType': response._headers.get(b'content-type', (None, 'application/octet-stream'))[(-1)]}, 
                         b'bodySize': responseHeadersSize + responseContentSize, 
                         b'redirectURL': response._headers.get(b'location', ('location', ''))[(-1)]}, 
           b'cache': {}, b'timings': {b'blocked': -1, 
                        b'dns': -1, 
                        b'connect': -1, 
                        b'send': 0, 
                        b'wait': int(round((datetime.utcnow() - startedDateTime).total_seconds() * 1000)), 
                        b'receive': 0, 
                        b'ssl': -1}})
        self.transport.send(alf.json)
        return response