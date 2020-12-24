# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\wsgize\__init__.py
# Compiled at: 2007-01-06 17:37:35
"""Middleware for WSGI-enabling Python callables including:

* An WSGI-compliant HTTP response generator
* A wrapper and decorator for making non-WSGI Python functions, callable
classes or methods into WSGI callables
* A secondary WSGI dispatcher.
* A decorator for autogenerating HTTP response codes, headers, and
  compliant iterators for WSGI callables
"""
__author__ = 'L.C. Rees (lcrees-at-gmail.com)'
__revision__ = '0.4'
import sys
from BaseHTTPServer import BaseHTTPRequestHandler as _bhrh
__all__ = [
 'response', 'Wsgize', 'WsgiWrap', 'WsgiRoute', 'wsgize', 'wsgiwrap', 'route', 'register']
routes = dict()

def register(name, application):
    """Registers a mapping of a name to an WSGI application.

    @param pattern URL pattern
    @param application WSGI application
    """
    routes[name] = application


def response(code):
    """Returns a WSGI response string.

    code HTTP response (integer)
    """
    return '%i %s' % (code, _bhrh.responses[code][0])


def route(name):
    """Callable decorator for an application with the secondary dispatcher."""

    def decorator(application):
        register(name, application)
        return application

    return decorator


def wsgize(**kw):
    """Decorator for Wsgize.

    @param application Application to decorate.
    """

    def decorator(application):
        return Wsgize(application, **kw)

    return decorator


def wsgiwrap(**kw):
    """Decorator for WsgiWrap.

    @param application Application to decorate.
    """

    def decorator(application):
        return WsgiWrap(application, **kw)

    return decorator


class Wsgize(object):
    """Autogenerates WSGI start_response callables, headers, and iterators for
    a WSGI application.
    """
    __module__ = __name__

    def __init__(self, app, **kw):
        self.application = app
        self.response = response(kw.get('response', 200))
        exheaders = kw.get('headers', dict())
        headers = list(((key, exheaders[key]) for key in exheaders))
        self.headers = [('Content-type', kw.get('mime', 'text/html'))] + headers
        self.exc_info = kw.get('exc_info', None)
        self.kwargkey = kw.get('kwargs', 'wsgize.kwargs')
        self.argkey = kw.get('args', 'wsgize.args')
        self.key = kw.get('routing_args', 'wsgiorg.routing_args')
        return

    def __call__(self, environ, start_response):
        """Passes WSGI params to a callable and autogenrates the start_response."""
        data = self.application(environ, start_response)
        start_response(self.response, self.headers, self.exc_info)
        if isinstance(data, basestring):
            data = [str(data)]
        if hasattr(data, '__iter__'):
            return data
        raise TypeError('Data returned by callable must be iterable.')


class WsgiWrap(Wsgize):
    """Makes arbitrary Python callables WSGI applications."""
    __module__ = __name__

    def __call__(self, environ, start_response):
        """Makes a Python callable a WSGI callable."""
        try:
            (args, kw) = environ.get(self.key)
        except ValueError:
            args = environ.get(self.argkey, ())
            kw = environ.get(self.kwargkey, {})

        if args and kw:
            data = self.application(*args, **kw)
        elif args:
            data = self.application(*args)
        elif kw:
            data = self.application(**kw)
        start_response(self.response, self.headers, self.exc_info)
        if isinstance(data, basestring):
            data = [str(data)]
        if hasattr(data, '__iter__'):
            return data
        raise TypeError('Data returned by callable must be iterable.')


class WsgiRoute(object):
    """Secondary WSGI dispatcher."""
    __module__ = __name__

    def __init__(self, table=None, **kw):
        """@param table Dictionary of names and callables."""
        if table is not None:
            self.table = table
        else:
            self.table = routes
        self.modpath = kw.get('modpath', '')
        self.key = kw.get('key', 'wsgize.callable')
        return

    def __call__(self, environ, start_response):
        """Passes WSGI params to a callable based on a keyword."""
        callback = self.lookup(environ[self.key])
        return callback(environ, start_response)

    def getapp(self, app):
        """Loads a callable based on its name

        @param app An WSGI application's name"""
        if self.modpath != '':
            app = ('.').join([self.modpath, app])
        dot = app.rindex('.')
        return getattr(__import__(app[:dot], '', '', ['']), app[dot + 1:])

    def lookup(self, kw):
        """Fetches an application based on keyword.

        @param kw Keyword
        """
        callback = self.table[kw]
        if hasattr(callback, '__call__'):
            return callback
        else:
            return self.getapp(callback)