# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\wsgiauth\basic.py
# Compiled at: 2006-10-30 14:23:34
"""HTTP Basic Authentication

This module implements basic HTTP authentication as described in
HTTP 1.0:

http://www.w3.org/Protocols/HTTP/1.0/draft-ietf-http-spec.html#BasicAA
"""
from wsgiauth.base import Scheme, HTTPAuth
__all__ = [
 'basic']

def basic(realm, authfunc, **kw):
    """Decorator for HTTP basic authentication."""

    def decorator(application):
        return HTTPAuth(application, realm, authfunc, BasicAuth, **kw)

    return decorator


class BasicAuth(Scheme):
    """Performs HTTP basic authentication."""
    __module__ = __name__
    authtype = 'basic'

    def _response(self, environ, start_response):
        """Default HTTP basic authentication response."""
        start_response('401 Unauthorized', [
         ('content-type', 'text/plain'), ('WWW-Authenticate', 'Basic realm="%s"' % self.realm)])
        return [
         self.message]

    def __call__(self, environ):
        authorization = environ.get('HTTP_AUTHORIZATION')
        if authorization is None:
            return self.response
        (authmeth, auth) = authorization.split(' ', 1)
        if authmeth.lower() != 'basic':
            return self.response
        auth = auth.strip().decode('base64')
        (username, password) = auth.split(':', 1)
        if self.authfunc(environ, username, password):
            return username
        return self.response