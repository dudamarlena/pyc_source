# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pyramid_turbolinks\__init__.py
# Compiled at: 2014-11-04 02:21:20
from __future__ import unicode_literals
__major__ = 1
__minor__ = 0
__revision__ = 0
__version_info__ = (
 __major__, __minor__, __revision__)
__version__ = b'%s.%s' % (__major__, __minor__)
try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

try:
    from pyramid.events import NewRequest, NewResponse
    from pyramid.httpexceptions import HTTPForbidden
except ImportError:
    pass

def same_origin(current_uri, redirect_uri):
    a = urlparse(current_uri)
    if not a.scheme:
        return True
    b = urlparse(redirect_uri)
    return (a.scheme, a.hostname, a.port) == (b.scheme, b.hostname, b.port)


def process_request(event):
    request = event.request
    referrer = request.environ.get(b'HTTP_X_XHR_REFERER')
    if referrer:
        request.environ[b'HTTP_REFERER'] = referrer


def process_response(event):
    request = event.request
    response = event.response
    referrer = request.headers.get(b'X-XHR-Referer')
    if not referrer:
        return response
    method = request.cookies.get(b'request_method')
    if not method or method != request.method:
        response.set_cookie(b'request_method', request.method)
    if response.location:
        request.session[b'_turbolinks_redirect_to'] = response.location
        if referrer and not same_origin(response.location, referrer):
            return HTTPForbidden()
    elif request.session.get(b'_turbolinks_redirect_to'):
        loc = request.session.pop(b'_turbolinks_redirect_to')
        response[b'X-XHR-Redirected-To'] = loc
    return response


def includeme(config):
    config.add_subscriber(process_request, NewRequest)
    config.add_subscriber(process_response, NewResponse)
    config.add_static_view(b'turbolinks', b'pyramid_turbolinks:static')