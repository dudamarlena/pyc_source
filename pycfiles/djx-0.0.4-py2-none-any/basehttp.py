# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/core/servers/basehttp.py
# Compiled at: 2019-02-14 00:35:17
"""
HTTP server that implements the Python WSGI protocol (PEP 333, rev 1.21).

Based on wsgiref.simple_server which is part of the standard library since 2.5.

This is a simple server for use in testing or debugging Django apps. It hasn't
been reviewed for security issues. DON'T USE IT FOR PRODUCTION USE!
"""
from __future__ import unicode_literals
import logging, socket, sys
from wsgiref import simple_server
from django.core.exceptions import ImproperlyConfigured
from django.core.wsgi import get_wsgi_application
from django.utils import six
from django.utils.module_loading import import_string
from django.utils.six.moves import socketserver
__all__ = ('WSGIServer', 'WSGIRequestHandler')
logger = logging.getLogger(b'django.server')

def get_internal_wsgi_application():
    """
    Loads and returns the WSGI application as configured by the user in
    ``settings.WSGI_APPLICATION``. With the default ``startproject`` layout,
    this will be the ``application`` object in ``projectname/wsgi.py``.

    This function, and the ``WSGI_APPLICATION`` setting itself, are only useful
    for Django's internal server (runserver); external WSGI servers should just
    be configured to point to the correct application object directly.

    If settings.WSGI_APPLICATION is not set (is ``None``), we just return
    whatever ``django.core.wsgi.get_wsgi_application`` returns.
    """
    from django.conf import settings
    app_path = getattr(settings, b'WSGI_APPLICATION')
    if app_path is None:
        return get_wsgi_application()
    else:
        try:
            return import_string(app_path)
        except ImportError as e:
            msg = b"WSGI application '%(app_path)s' could not be loaded; Error importing module: '%(exception)s'" % {b'app_path': app_path, 
               b'exception': e}
            six.reraise(ImproperlyConfigured, ImproperlyConfigured(msg), sys.exc_info()[2])

        return


def is_broken_pipe_error():
    exc_type, exc_value = sys.exc_info()[:2]
    return issubclass(exc_type, socket.error) and exc_value.args[0] == 32


class WSGIServer(simple_server.WSGIServer, object):
    """BaseHTTPServer that implements the Python WSGI protocol"""
    request_queue_size = 10

    def __init__(self, *args, **kwargs):
        if kwargs.pop(b'ipv6', False):
            self.address_family = socket.AF_INET6
        self.allow_reuse_address = kwargs.pop(b'allow_reuse_address', True)
        super(WSGIServer, self).__init__(*args, **kwargs)

    def handle_error(self, request, client_address):
        if is_broken_pipe_error():
            logger.info(b'- Broken pipe from %s\n', client_address)
        else:
            super(WSGIServer, self).handle_error(request, client_address)


class ServerHandler(simple_server.ServerHandler, object):

    def handle_error(self):
        if not is_broken_pipe_error():
            super(ServerHandler, self).handle_error()


class WSGIRequestHandler(simple_server.WSGIRequestHandler, object):

    def address_string(self):
        return self.client_address[0]

    def log_message(self, format, *args):
        extra = {b'request': self.request, 
           b'server_time': self.log_date_time_string()}
        if args[1][0] == b'4':
            if args[0].startswith(str(b'\x16\x03')):
                extra[b'status_code'] = 500
                logger.error(b"You're accessing the development server over HTTPS, but it only supports HTTP.\n", extra=extra)
                return
        if args[1].isdigit() and len(args[1]) == 3:
            status_code = int(args[1])
            extra[b'status_code'] = status_code
            if status_code >= 500:
                level = logger.error
            elif status_code >= 400:
                level = logger.warning
            else:
                level = logger.info
        else:
            level = logger.info
        level(format, extra=extra, *args)

    def get_environ(self):
        for k, v in self.headers.items():
            if b'_' in k:
                del self.headers[k]

        return super(WSGIRequestHandler, self).get_environ()

    def handle(self):
        """Copy of WSGIRequestHandler, but with different ServerHandler"""
        self.raw_requestline = self.rfile.readline(65537)
        if len(self.raw_requestline) > 65536:
            self.requestline = b''
            self.request_version = b''
            self.command = b''
            self.send_error(414)
            return
        if not self.parse_request():
            return
        handler = ServerHandler(self.rfile, self.wfile, self.get_stderr(), self.get_environ())
        handler.request_handler = self
        handler.run(self.server.get_app())


def run(addr, port, wsgi_handler, ipv6=False, threading=False, server_cls=WSGIServer):
    server_address = (addr, port)
    if threading:
        httpd_cls = type(str(b'WSGIServer'), (socketserver.ThreadingMixIn, server_cls), {})
    else:
        httpd_cls = server_cls
    httpd = httpd_cls(server_address, WSGIRequestHandler, ipv6=ipv6)
    if threading:
        httpd.daemon_threads = True
    httpd.set_app(wsgi_handler)
    httpd.serve_forever()