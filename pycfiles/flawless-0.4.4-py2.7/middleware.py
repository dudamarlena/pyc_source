# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/flawless/client/middleware.py
# Compiled at: 2017-12-21 14:51:54
import socket, sys
from future.utils import raise_
try:
    import webob
except:
    pass

import flawless.client

class FlawlessMiddleware(object):
    """Middleware records errors to the error backend"""

    def __init__(self, app):
        self.app = app
        self.hostname = socket.gethostname()

    def __call__(self, environ, start_response):
        try:
            return self.app(environ, start_response)
        except:
            type, value, tb = sys.exc_info()
            reconstructed_req = self._reconstruct_request(environ)
            flawless.client.record_error(hostname=self.hostname, tb=tb, exception_message=repr(value), additional_info=reconstructed_req)
            raise_(value, None, tb)

        return

    def _reconstruct_request(self, environ):
        request_str = ''
        if 'webob' in globals():
            request_str = str(webob.Request(environ))[:2000]
        else:
            req_parts = []
            method = environ.get('REQUEST_METHOD', '')
            path = environ.get('PATH_INFO', '')
            path += '?' * bool(environ.get('QUERY_STRING')) + environ.get('QUERY_STRING', '')
            req_parts.append('%s %s %s' % (method, path, environ.get('SERVER_PROTOCOL', '')))
            req_parts.append('Host: %s' % environ.get('HTTP_HOST', ''))
            req_parts.append('Referer: %s' % environ.get('HTTP_REFERER', ''))
            req_parts.append('Cookie: %s' % environ.get('HTTP_COOKIE', ''))
            req_parts.append('Content-Length: %s' % environ.get('CONTENT_LENGTH', ''))
            req_parts.append('User-Agent: %s' % environ.get('HTTP_USER_AGENT', ''))
            request_str = ('\n').join(req_parts)
        return request_str