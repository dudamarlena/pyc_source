# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\wsgiauth\url.py
# Compiled at: 2006-10-30 14:23:34
"""Persistent authentication tokens in URL query components."""
import cgi
from wsgiauth.base import BaseAuth
from wsgiauth.util import Redirect, geturl
__all__ = [
 'URLAuth', 'urlauth']

def urlauth(authfunc, **kw):
    """Decorator for persistent authentication tokens in URLs."""

    def decorator(application):
        return URLAuth(application, authfunc, **kw)

    return decorator


class URLAuth(BaseAuth):
    """Persists authentication tokens in URL query components."""
    __module__ = __name__
    authtype = 'url'

    def __init__(self, application, authfunc, **kw):
        super(URLAuth, self).__init__(application, authfunc, **kw)
        self.redirect = kw.get('redirect', Redirect)

    def authenticate(self, environ):
        """Authenticates a token embedded in a query component."""
        try:
            query = cgi.parse_qs(environ['QUERY_STRING'])
            return self._authtoken(environ, query[self.name][0])
        except KeyError:
            return False

    def generate(self, env):
        """Embeds authentication token in query component."""
        env['QUERY_STRING'] = ('=').join([self.name, self._gettoken(env)])

    def initial(self, environ, start_response):
        self.generate(environ)
        redirect = self.redirect(geturl(environ))
        return redirect(environ, start_response)