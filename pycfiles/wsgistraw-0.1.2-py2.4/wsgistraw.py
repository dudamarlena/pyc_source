# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\wsgistraw.py
# Compiled at: 2007-09-21 17:35:50
"""decorators for WSGI without start_response and write

wsgistraw is a tiny Python library that simplifies coding WSGI applications
and middleware by removing start_response and write from signatures of
functions. This leads to a signature like:

def app(environ):
    return "200 OK", [("Content-Type", "text/plain")], ["Hello World!"]

That is, return a three-tuple of (status, headers, response).

Project site: http://abstracthack.wordpress.com/wsgistraw

See also:

* http://www.wsgi.org/wsgi/WSGI_2.0
* http://www.python.org/dev/peps/pep-0333/ 
"""
__all__ = [
 'mid_factory', 'app', 'app_proxy']
__author__ = 'Andrey Nordin <http://claimid.com/anrienord>'
__version__ = '0.1.2'
from types import FunctionType, MethodType

def app(app):
    """Decorates WSGI application callables (both functions and methods)."""

    def decorator(*args):
        if len(args) == 2:
            (environ, start_response) = args
            (status, headers, response) = app(environ)
        elif len(args) == 3:
            (self, environ, start_response) = args
            (status, headers, response) = app(self, environ)
        else:
            raise TypeError('app() takes 2 or 3 arguments (%d given)' % len(args))
        start_response(status, headers)
        return response

    return decorator


def mid_factory(mid_factory):
    """Decorates WSGI middleware factories, i. e. callables that accept a WSGI
    application as their first positional parameter and return a middleware
    callable."""

    def decorator(app, *args, **kwargs):
        return _mid_proxy(mid_factory, app, *args, **kwargs)

    return decorator


class app_proxy(object):
    """Replaces a WSGI application callable on the caller side, returns the
    application with the simplified signature."""
    __module__ = __name__

    def __init__(self, app):
        self.app = app

    def __call__(self, environ):
        headers = []
        r = []

        def start_response(status, response_headers, exc_info=None):
            if exc_info:
                try:
                    raise exc_info[0], exc_info[1], exc_info[2]
                finally:
                    exc_info = None
            headers[:] = [
             status, response_headers]
            return r.append

        response = self.app(environ, start_response)
        if r:
            r.extend(response)
            if hasattr(response, 'close'):
                response.close()
            response = r
        if not headers:
            response = _head_iter(response.next(), response)
        return (
         headers[0], headers[1], response)


class _mid_proxy(object):
    __module__ = __name__

    def __init__(self, mid_factory, app, *args, **kwargs):
        self.middleware = mid_factory(app_proxy(app), *args, **kwargs)

    def __call__(self, environ, start_response):
        (status, headers, response) = self.middleware(environ)
        start_response(status, headers)
        return response


class _head_iter(object):
    __module__ = __name__

    def __init__(self, head, iter):
        self.head_sent = False
        self.head = head
        self.iter = iter
        if hasattr(iter, 'close'):
            self.close = iter.close

    def __iter__(self):
        return self

    def next(self):
        if self.head_sent:
            return self.iter.next()
        else:
            self.head_sent = True
            return self.head