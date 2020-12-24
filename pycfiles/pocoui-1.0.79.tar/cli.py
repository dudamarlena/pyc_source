# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pocoo/wrappers/cli.py
# Compiled at: 2006-12-26 17:18:07
__doc__ = "\n    pocoo.wrappers.cli\n    ~~~~~~~~~~~~~~~~~~\n\n    Pocoo command line interpreter utils.\n\n    Basic Usage::\n\n        >>> from pocoo.wrappers.cli import *\n        >>> ctx = create_context('instance/')\n        >>> core = import_package(ctx, 'core')\n        >>> core\n        <module 'pocoo.pkg___57736.core' from '../core.pkg/__init__.pyc'>\n        >>> ctx.cfg.root\n        '/home/blackbird/Developement/pocoo/trunk/instance'\n        >>> ctx.cfg.get('database', 'uri')\n        u'sqlite:///tmp/test.db'\n        >>> app = create_application(ctx)\n        >>> app\n        <function app at 0xb760f8ec>\n        >>> req = create_request(app)\n        >>> req\n        <Request ''>\n        >>> req.user\n        <User -1: u'anonymous' *>\n        >>> execute(app)\n        Status: 200 OK\n        Content-Type: text/html\n        ...\n\n    :copyright: 2006 by Armin Ronacher.\n    :license: GNU GPL, see LICENSE for more details.\n"
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