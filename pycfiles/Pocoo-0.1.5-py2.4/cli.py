# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pocoo/wrappers/cli.py
# Compiled at: 2006-12-26 17:18:07
"""
    pocoo.wrappers.cli
    ~~~~~~~~~~~~~~~~~~

    Pocoo command line interpreter utils.

    Basic Usage::

        >>> from pocoo.wrappers.cli import *
        >>> ctx = create_context('instance/')
        >>> core = import_package(ctx, 'core')
        >>> core
        <module 'pocoo.pkg___57736.core' from '../core.pkg/__init__.pyc'>
        >>> ctx.cfg.root
        '/home/blackbird/Developement/pocoo/trunk/instance'
        >>> ctx.cfg.get('database', 'uri')
        u'sqlite:///tmp/test.db'
        >>> app = create_application(ctx)
        >>> app
        <function app at 0xb760f8ec>
        >>> req = create_request(app)
        >>> req
        <Request ''>
        >>> req.user
        <User -1: u'anonymous' *>
        >>> execute(app)
        Status: 200 OK
        Content-Type: text/html
        ...

    :copyright: 2006 by Armin Ronacher.
    :license: GNU GPL, see LICENSE for more details.
"""
import sys, os, urllib
__all__ = [
 'create_request', 'makelocal']

class CliServer(object):
    __module__ = __name__

    def __init__(self, application, params=None, query_string='', path_info='', cookie='', stream=None):
        self.application = application
        if params is None:
            params = {}
        self.query_string = urllib.urlencode(params) or query_string
        self.path_info = path_info
        self.cookie = cookie
        self.stream = stream or sys.stdout
        return

    def run(self, partial=False):
        environ = dict(os.environ.items())
        environ.update({'wsgi.input': sys.stdin, 'wsgi.errors': sys.stderr, 'wsgi.version': (1, 0), 'wsgi.multithread': False, 'wsgi.multiprocess': True, 'wsgi.run_once': False, 'QUERY_STRING': self.query_string, 'PATH_INFO': self.path_info, 'SCRIPT_NAME': '', 'HTTP_COOKIE': self.cookie, 'HTTP_HOST': 'localhost', 'SERVER_NAME': 'localhost', 'SERVER_ADDR': '127.0.0.1', 'SERVER_PORT': '8080', 'REMOTE_ADDR': '127.0.0.1', 'REQUEST_METHOD': 'GET'})
        if environ.get('HTTPS', 'off') in ('on', '1'):
            environ['wsgi.url_scheme'] = 'https'
        else:
            environ['wsgi.url_scheme'] = 'http'
        headers_set = []
        headers_sent = []
        last_char = []

        def write(data):
            if not headers_set:
                raise AssertionError('write() before start_response()')
            elif not headers_sent:
                (status, response_headers) = headers_sent[:] = headers_set
                self.stream.write('Status: %s\r\n' % status)
                for header in response_headers:
                    sys.stdout.write('%s: %s\r\n' % header)

                self.stream.write('\r\n')
            if data:
                last_char[:] = [
                 data[(-1)]]
            self.stream.write(data)
            self.stream.flush()

        def start_response(status, response_headers, exc_info=None):
            if exc_info:
                try:
                    if headers_sent:
                        raise exc_info[0], exc_info[1], exc_info[2]
                finally:
                    exc_info = None
            elif headers_set:
                raise AssertionError('Headers already set!')
            headers_set[:] = [status, response_headers]
            return write

        result = self.application(environ, start_response)
        try:
            for data in iter(result):
                if partial:
                    return environ
                if data:
                    write(data)

            if partial:
                return environ
            if not headers_sent:
                write('')
        finally:
            if hasattr(result, 'close'):
                result.close()
        if not last_char or last_char != '\n':
            self.stream.write('\n')
        return


def create_request(ctx, **kwargs):
    """Create a new application object and return the request."""
    srv = CliServer(ctx.app, **kwargs)
    environ = srv.run(partial=True)
    request = environ['colubrid.request']
    return request


def makelocal(obj):
    """
    copy a obj dict into the current namespace
    """
    frm = sys._getframe(1)
    if not isinstance(obj, dict):
        obj = obj.__dict__
    for (name, value) in obj.iteritems():
        if not name.startswith('_'):
            frm.f_locals[name] = value