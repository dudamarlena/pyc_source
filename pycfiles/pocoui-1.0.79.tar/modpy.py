# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pocoo/wrappers/modpy.py
# Compiled at: 2006-12-26 17:18:07
__doc__ = '\n    pocoo.wrappers.modpy\n    ~~~~~~~~~~~~~~~~~~~~\n\n    Mod Python WSGI Gateway\n\n    This module implements a mod_python wsgi gateway proving full compatibility\n    with wsgi 1.0\n\n    For a short introduction how to use your pocoo instance over mod_python,\n    see `pocoo.wrappers`.\n\n    :copyright: 2006 by Armin Ronacher.\n    :license: GNU GPL, see LICENSE for more details.\n'
from mod_python import apache

class WSGIServer(object):
    __module__ = __name__

    def __init__(self, application):
        self._application = application

    def run(self, req):
        environ = dict(apache.build_cgi_env(req))
        options = req.get_options()

        class InputStream(object):
            __module__ = __name__

            def close(self):
                pass

            def read(self, size=-1):
                return req.read(size)

            def readline(self):
                return req.readline()

            def readlines(self, hint=-1):
                return req.readlines(hint)

            def flush(self):
                pass

            def write(self, s):
                pass

            def writelines(self, seq):
                pass

            def __iter__(self):
                while True:
                    line = self.readline()
                    if not line:
                        return
                    yield line

        class ErrorStream(object):
            __module__ = __name__

            def read(self, size=-1):
                return ''

            def readline(self):
                return '\n'

            def readlines(self, hint=-1):
                return []

            def flush(self):
                pass

            def write(self, s):
                req.log_error(s)

            def writelines(self, seq):
                for item in seq:
                    req.log_error(item)

            def __iter__(self):
                return iter(int, 0)

        try:
            threaded = apache.mpm_query(apache.AP_MPMQ_IS_THREADED)
            forked = apache.mpm_query(apache.AP_MPMQ_IS_FORKED)
        except AttributeError:
            threaded = options.get('multithread', '').lower() == 'on'
            forked = options.get('multiprocess', '').lower() == 'on'

        if options.get('untouched_scriptname', '').lower() not in ('1', 'on', 'yes'):
            path_info = None
            if 'PATH_TRANSLATED' in environ:
                (_, script_name, prefix) = environ['SCRIPT_NAME'].split('/', 2)
                script_name = '/' + script_name
                path_info = '/' + prefix + environ.get('PATH_INFO', '')
            elif 'PATH_INFO' not in environ:
                bits = environ['SCRIPT_NAME'].split('/')
                script_name = ('/').join(bits[:-1])
                path_info = '/' + bits[(-1)]
            if script_name == '/':
                script_name = ''
            environ['SCRIPT_NAME'] = script_name
            if path_info:
                environ['PATH_INFO'] = path_info
        if environ.get('HTTPS', '').lower() in ('1', 'yes', 'on'):
            url_scheme = 'https'
        else:
            url_scheme = 'http'
        environ.update({'wsgi.input': InputStream(), 'wsgi.error': ErrorStream(), 'wsgi.version': (1, 0), 'wsgi.run_once': False, 'wsgi.url_scheme': url_scheme, 'wsgi.multithread': threaded, 'wsgi.multiprocess': forked})
        req.content_type = 'text/plain'
        headers_set = []
        headers_sent = []

        def write(data):
            if not headers_set:
                raise AssertionError('write() before start_response()')
            elif not headers_sent:
                (status, response_headers) = headers_sent[:] = headers_set
                req.status = int(status[:3])
                for (key, value) in response_headers:
                    if key.lower() == 'content-length':
                        req.set_content_length(int(value))
                    elif key.lower() == 'content-type':
                        req.content_type = value
                    else:
                        req.headers_out.add(key, value)

            req.write(data)

        def start_response(status, response_headers, exc_info=None):
            if exc_info:
                try:
                    if headers_sent:
                        raise exc_info[0], exc_info[1], exc_info[2]
                finally:
                    exc_info = None
            elif headers_set:
                raise AssertionError('Headers already set!')
            headers_set[:] = [
             status, response_headers]
            return write

        result = self._application(environ, start_response)
        try:
            for data in result:
                if data:
                    write(data)

            if not headers_sent:
                write('')
        finally:
            if hasattr(result, 'close'):
                result.close()
            return apache.OK
        return


from pocoo.context import ApplicationContext
server = None

def handler(req):
    """
    A mod_python compatible handler for pocoo.
    Use it by putting this into your .htaccess::

        SetHandler python-program
        PythonHandler pocoo.wrappers.modpy::handler
        PythonOption instancepath /path/to/pocoo/instance
    """
    global server
    if not server:
        options = req.get_options()
        instancepath = options['instancepath']
        context = ApplicationContext(instancepath)
        server = WSGIServer(context)
    return server.run(req)