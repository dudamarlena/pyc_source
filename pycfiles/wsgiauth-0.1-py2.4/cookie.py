# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\wsgiauth\cookie.py
# Compiled at: 2006-10-30 14:23:34
"""WSGI middleware for persistent authentication tokens in cookies."""
from Cookie import SimpleCookie
from wsgiauth.base import BaseAuth
__all__ = [
 'Cookie', 'cookie']

def cookie(authfunc, **kw):
    """Decorator for persistent authentication tokens in cookies."""

    def decorator(application):
        return Cookie(application, authfunc, **kw)

    return decorator


class Cookie(BaseAuth):
    """Persists authentication tokens in HTTP cookies."""
    __module__ = __name__
    authtype = 'cookie'

    def __init__(self, application, authfunc, **kw):
        super(Cookie, self).__init__(application, authfunc, **kw)
        self.domain = kw.get('domain')
        self.age = kw.get('age', 7200)
        self.path, self.comment = kw.get('path', '/'), kw.get('comment')

    def authenticate(self, environ):
        """Authenticates a token embedded in a cookie."""
        try:
            cookies = SimpleCookie(environ['HTTP_COOKIE'])
            scookie = cookies[self.name]
            auth = self._authtoken(environ, scookie.value)
            if not auth:
                scookie[scookie.value]['expires'] = -365 * 24 * 60 * 60
                scookie[scookie.value]['max-age'] = 0
            return auth
        except KeyError:
            return False

    def generate(self, environ):
        """Returns an authentication token embedded in a cookie."""
        scookie = SimpleCookie()
        scookie[self.name] = self._gettoken(environ)
        scookie[self.name]['path'] = self.path
        scookie[self.name]['max-age'] = self.age
        if self.domain is not None:
            scookie[self.name]['domain'] = self.domain
        if self.comment is not None:
            scookie[self.name]['comment'] = self.comment
        if environ['wsgi.url_scheme'] == 'https':
            scookie[self.name]['secure'] = ''
        return scookie[self.name].OutputString()

    def initial(self, environ, start_response):
        """Initial response to a request."""

        def cookie_response(status, headers, exc_info=None):
            headers.append(('Set-Cookie', self.generate(environ)))
            return start_response(status, headers, exc_info)

        return self.application(environ, cookie_response)