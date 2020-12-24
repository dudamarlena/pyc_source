# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/core/servers/basehttp.py
# Compiled at: 2018-07-11 18:15:30
"""
HTTP server that implements the Python WSGI protocol (PEP 333, rev 1.21).

Based on wsgiref.simple_server which is part of the standard library since 2.5.

This is a simple server for use in testing or debugging Django apps. It hasn't
been reviewed for security issues. DON'T USE IT FOR PRODUCTION USE!
"""
from __future__ import unicode_literals
import os, socket, sys, traceback
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

from django.utils.six.moves import socketserver
from wsgiref import simple_server
from wsgiref.util import FileWrapper
import django
from django.core.exceptions import ImproperlyConfigured
from django.core.management.color import color_style
from django.core.wsgi import get_wsgi_application
from django.utils.importlib import import_module
__all__ = [
 b'WSGIServer', b'WSGIRequestHandler']

def get_internal_wsgi_application():
    """
    Loads and returns the WSGI application as configured by the user in
    ``settings.WSGI_APPLICATION``. With the default ``startproject`` layout,
    this will be the ``application`` object in ``projectname/wsgi.py``.

    This function, and the ``WSGI_APPLICATION`` setting itself, are only useful
    for Django's internal servers (runserver, runfcgi); external WSGI servers
    should just be configured to point to the correct application object
    directly.

    If settings.WSGI_APPLICATION is not set (is ``None``), we just return
    whatever ``django.core.wsgi.get_wsgi_application`` returns.

    """
    from django.conf import settings
    app_path = getattr(settings, b'WSGI_APPLICATION')
    if app_path is None:
        return get_wsgi_application()
    else:
        module_name, attr = app_path.rsplit(b'.', 1)
        try:
            mod = import_module(module_name)
        except ImportError as e:
            raise ImproperlyConfigured(b"WSGI application '%s' could not be loaded; could not import module '%s': %s" % (
             app_path, module_name, e))

        try:
            app = getattr(mod, attr)
        except AttributeError as e:
            raise ImproperlyConfigured(b"WSGI application '%s' could not be loaded; can't find '%s' in module '%s': %s" % (
             app_path, attr, module_name, e))

        return app


class ServerHandler(simple_server.ServerHandler, object):
    error_status = str(b'500 INTERNAL SERVER ERROR')

    def write(self, data):
        """'write()' callable as specified by PEP 3333"""
        assert isinstance(data, bytes), b'write() argument must be bytestring'
        if not self.status:
            raise AssertionError(b'write() before start_response()')
        elif not self.headers_sent:
            self.bytes_sent = len(data)
            self.send_headers()
        else:
            self.bytes_sent += len(data)
        length = len(data)
        if length > 33554432:
            offset = 0
            while offset < length:
                chunk_size = min(33554432, length)
                self._write(data[offset:offset + chunk_size])
                self._flush()
                offset += chunk_size

        else:
            self._write(data)
            self._flush()

    def error_output(self, environ, start_response):
        super(ServerHandler, self).error_output(environ, start_response)
        return [(b'\n').join(traceback.format_exception(*sys.exc_info()))]

    def finish_response(self):
        try:
            if not self.result_is_file() or not self.sendfile():
                for data in self.result:
                    self.write(data)

                self.finish_content()
        finally:
            self.close()


class WSGIServer(simple_server.WSGIServer, object):
    """BaseHTTPServer that implements the Python WSGI protocol"""

    def __init__(self, *args, **kwargs):
        if kwargs.pop(b'ipv6', False):
            self.address_family = socket.AF_INET6
        super(WSGIServer, self).__init__(*args, **kwargs)

    def server_bind(self):
        """Override server_bind to store the server name."""
        super(WSGIServer, self).server_bind()
        self.setup_environ()


class WSGIRequestHandler(simple_server.WSGIRequestHandler, object):

    def __init__(self, *args, **kwargs):
        from django.conf import settings
        self.admin_static_prefix = urljoin(settings.STATIC_URL, b'admin/')
        self.path = b''
        self.style = color_style()
        super(WSGIRequestHandler, self).__init__(*args, **kwargs)

    def address_string(self):
        return self.client_address[0]

    def log_message(self, format, *args):
        if self.path.startswith(self.admin_static_prefix) or self.path == b'/favicon.ico':
            return
        msg = b'[%s] %s\n' % (self.log_date_time_string(), format % args)
        if args[1][0] == b'2':
            msg = self.style.HTTP_SUCCESS(msg)
        elif args[1][0] == b'1':
            msg = self.style.HTTP_INFO(msg)
        elif args[1] == b'304':
            msg = self.style.HTTP_NOT_MODIFIED(msg)
        elif args[1][0] == b'3':
            msg = self.style.HTTP_REDIRECT(msg)
        elif args[1] == b'404':
            msg = self.style.HTTP_NOT_FOUND(msg)
        elif args[1][0] == b'4':
            msg = self.style.HTTP_BAD_REQUEST(msg)
        else:
            msg = self.style.HTTP_SERVER_ERROR(msg)
        sys.stderr.write(msg)


def run(addr, port, wsgi_handler, ipv6=False, threading=False):
    server_address = (addr, port)
    if threading:
        httpd_cls = type(str(b'WSGIServer'), (socketserver.ThreadingMixIn, WSGIServer), {})
    else:
        httpd_cls = WSGIServer
    httpd = httpd_cls(server_address, WSGIRequestHandler, ipv6=ipv6)
    httpd.set_app(wsgi_handler)
    httpd.serve_forever()