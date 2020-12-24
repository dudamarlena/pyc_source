# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dap/util/wsgi_intercept.py
# Compiled at: 2008-03-31 07:43:21
"""
wsgi_intercept.WSGI_HTTPConnection is a replacement for
httplib.HTTPConnection that intercepts certain HTTP connections into a
WSGI application.

Use 'add_wsgi_intercept' and 'remove_wsgi_intercept' to control this behavior.
"""
import sys
from httplib import HTTPConnection
from cStringIO import StringIO
import traceback
debuglevel = 0
_wsgi_intercept = {}

def add_wsgi_intercept(host, port, app_create_fn, script_name=''):
    """
    Add a WSGI intercept call for host:port, using the app returned
    by app_create_fn with a SCRIPT_NAME of 'script_name' (default '').
    """
    _wsgi_intercept[(host, port)] = (
     app_create_fn, script_name)


def remove_wsgi_intercept(host, port):
    """
    Remove the WSGI intercept call for (host, port).
    """
    key = (
     host, port)
    if _wsgi_intercept.has_key(key):
        del _wsgi_intercept[key]


def make_environ(inp, host, port, script_name):
    """
    Take 'inp' as if it were HTTP-speak being received on host:port,
    and parse it into a WSGI-ok environment dictionary.  Return the
    dictionary.

    Set 'SCRIPT_NAME' from the 'script_name' input, and, if present,
    remove it from the beginning of the PATH_INFO variable.
    """
    environ = {}
    method_line = inp.readline()
    content_type = None
    content_length = None
    cookies = []
    for line in inp:
        if not line.strip():
            break
        (k, v) = line.strip().split(':', 1)
        v = v.lstrip()
        if k.lower() == 'content-type':
            content_type = v
        elif k.lower() == 'content-length':
            content_length = v
        elif k.lower() == 'cookie' or k.lower() == 'cookie2':
            cookies.append(v)
        else:
            h = k.upper()
            h = h.replace('-', '_')
            environ['HTTP_' + h] = v
        if debuglevel >= 2:
            print 'HEADER:', k, v

    if debuglevel >= 2:
        print 'METHOD LINE:', method_line
    (method, url, protocol) = method_line.split(' ')
    if not url.startswith(script_name):
        script_name = ''
    else:
        url = url[len(script_name):]
    url = url.split('?', 1)
    path_info = url[0]
    query_string = ''
    if len(url) == 2:
        query_string = url[1]
    if debuglevel:
        print 'method: %s; script_name: %s; path_info: %s; query_string: %s' % (method, script_name, path_info, query_string)
    r = inp.read()
    inp = StringIO(r)
    environ.update({'wsgi.version': (1, 0), 'wsgi.url_scheme': 'http', 
       'wsgi.input': inp, 
       'wsgi.errors': StringIO(), 
       'wsgi.multithread': 0, 
       'wsgi.multiprocess': 0, 
       'wsgi.run_once': 0, 
       'REQUEST_METHOD': method, 
       'SCRIPT_NAME': script_name, 
       'PATH_INFO': path_info, 
       'SERVER_NAME': host, 
       'SERVER_PORT': str(port), 
       'SERVER_PROTOCOL': protocol, 
       'REMOTE_ADDRESS': '127.0.0.1'})
    if query_string:
        environ['QUERY_STRING'] = query_string
    if content_type:
        environ['CONTENT_TYPE'] = content_type
        if debuglevel >= 2:
            print 'CONTENT-TYPE:', content_type
    if content_length:
        environ['CONTENT_LENGTH'] = content_length
        if debuglevel >= 2:
            print 'CONTENT-LENGTH:', content_length
    if cookies:
        environ['HTTP_COOKIE'] = ('; ').join(cookies)
    if debuglevel:
        print 'WSGI environ dictionary:', environ
    return environ


class wsgi_fake_socket:
    """
    Handle HTTP traffic and stuff into a WSGI application object instead.

    Note that this class assumes:
    
     1. 'makefile' is called (by the response class) only after all of the
        data has been sent to the socket by the request class;
     2. non-persistent (i.e. non-HTTP/1.1) connections.
    """

    def __init__(self, app, host, port, script_name):
        self.app = app
        self.host = host
        self.port = port
        self.script_name = script_name
        self.inp = StringIO()
        self.results = None
        self.output = StringIO()
        return

    def makefile(self, *args, **kwargs):
        """
        'makefile' is called by the HTTPResponse class once all of the
        data has been written.  So, in this interceptor class, we need to:
        
          1. build a start_response function that grabs all the headers
             returned by the WSGI app;
          2. create a wsgi.input file object 'inp', containing all of the
             traffic;
          3. build an environment dict out of the traffic in inp;
          4. run the WSGI app & grab the result object;
          5. concatenate & return the result(s) read from the result object.

        @CTB: 'start_response' should return a function that writes
        directly to self.result, too.
        """

        def start_response(status, headers, exc_info=None):
            self.output.write('HTTP/1.0 ' + status + '\n')
            for (k, v) in headers:
                self.output.write('%s: %s\n' % (k, v))

            self.output.write('\n')

        inp = StringIO(self.inp.getvalue())
        environ = make_environ(inp, self.host, self.port, self.script_name)
        self.result = self.app(environ, start_response)
        for data in self.result:
            self.output.write(data)

        if debuglevel >= 2:
            print '***', self.output.getvalue(), '***'
        return StringIO(self.output.getvalue())

    def sendall(self, str):
        """
        Save all the traffic to self.inp.
        """
        if debuglevel >= 2:
            print '>>>', str, '>>>'
        self.inp.write(str)

    def close(self):
        """Do nothing, for now."""
        pass


class WSGI_HTTPConnection(HTTPConnection):
    """
    Intercept all traffic to certain hosts & redirect into a WSGI
    application object.
    """

    def get_app(self, host, port):
        """
        Return the app object for the given (host, port).
        """
        key = (
         host, int(port))
        (app, script_name) = (None, None)
        if _wsgi_intercept.has_key(key):
            (app_fn, script_name) = _wsgi_intercept[key]
            app = app_fn()
        return (app, script_name)

    def connect(self):
        """
        Override the connect() function to intercept calls to certain
        host/ports.
        """
        if debuglevel:
            sys.stderr.write('connect: %s, %s\n' % (self.host, self.port))
        try:
            (app, script_name) = self.get_app(self.host, self.port)
            if app:
                if debuglevel:
                    sys.stderr.write('INTERCEPTING call to %s:%s\n' % (
                     self.host, self.port))
                self.sock = wsgi_fake_socket(app, self.host, self.port, script_name)
            else:
                HTTPConnection.connect(self)
        except Exception, e:
            if debuglevel:
                traceback.print_exc()
            raise