# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\wsgiauth\ip.py
# Compiled at: 2006-10-30 14:23:34
"""Authenticate an IP address."""
from wsgiauth.util import Forbidden
__all__ = [
 'IP', 'ip']

def ip(authfunc, **kw):
    """Decorator for IP address-based authentication."""

    def decorator(application):
        return IP(application, authfunc, **kw)

    return decorator


class IP(object):
    """On each request, `REMOTE_ADDR` is authenticated and access allowed based
    on IP address.
    """
    __module__ = __name__

    def __init__(self, app, authfunc, **kw):
        self.app, self.authfunc = app, authfunc
        self.response = kw.get('response', Forbidden())

    def __call__(self, environ, start_response):
        ipaddr = environ.get('REMOTE_ADDR')
        if not self.authfunc(environ, ipaddr):
            return self.response(environ, start_response)
        return self.app(environ, start_response)