# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/universalcore/unicore.distribute/unicore/distribute/api/proxy.py
# Compiled at: 2016-05-07 05:25:40
from urlparse import urljoin
from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound
import requests

class Proxy(object):

    def __init__(self, upstream_url):
        self.upstream_url = upstream_url

    def __call__(self, request):
        view = ProxyView(request, self.upstream_url)
        handler = getattr(view, 'do_%s' % (request.method,), HTTPNotFound)
        return handler()


class ProxyView(object):

    def __init__(self, request, upstream_url):
        self.request = request
        self.upstream_url = upstream_url

    def url(self):
        return urljoin(self.upstream_url, self.request.matchdict['parts'])

    def mk_request(self, *args, **kwargs):
        return requests.request(*args, **kwargs)

    def mk_response(self, response):
        return Response(body=response.text, status=response.status_code, headerlist=response.headers.items(), content_type=response.headers['Content-Type'], charset=response.encoding)

    def do_request(self):
        return self.mk_response(self.mk_request(self.request.method, self.url(), data=self.request.body))

    def do_POST(self):
        return self.do_request()

    def do_DELETE(self):
        return self.do_request()

    def do_PUT(self):
        return self.do_request()

    def do_GET(self):
        return self.do_request()

    def do_HEAD(self):
        return self.do_request()