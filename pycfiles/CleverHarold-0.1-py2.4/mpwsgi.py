# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/harold/lib/mpwsgi.py
# Compiled at: 2006-08-02 05:57:51
from mod_python import apache
apache_request_key = 'apache.request'

class StdIn:
    """ Wrapper for stdin

    @param req mod_python request object
    """
    __module__ = __name__

    def __init__(self, req):
        self.req = req

    def close(self):
        pass

    def read(self, size=-1):
        return self.req.read(size)

    def readline(self, size=-1):
        return self.req.readline(size)

    def readlines(self, hint=-1):
        return self.req.readlines(hint)

    def __iter__(self):
        line = self.readline()
        while line:
            yield line
            line = self.readline()


class StdErr:
    """ Wrapper for stderr

    @param req mod_python request object
    """
    __module__ = __name__

    def __init__(self, req):
        self.req = req

    def flush(self):
        pass

    def write(self, msg):
        self.req.log_error(msg)

    def writelines(self, seq):
        self.write(('').join(seq))


class WsgiAdapter:
    """ Adapts apache mod_python requests to WSGI applications

    @param req mod_python request object
    """
    __module__ = __name__

    def __init__(self, req):
        self.environ = env = dict(apache.build_cgi_env(req))
        self.request = env[apache_request_key] = req
        self.started = False
        self.options = options = req.get_options()
        if 'wsgi.scr' in options:
            env['SCRIPT_NAME'] = scr = options['wsgi.scr']
            env['PATH_INFO'] = req.uri[len(scr):]
        else:
            env['SCRIPT_NAME'] = ''
            env['PATH_INFO'] = req.uri
        env['wsgi.errors'] = StdErr(req)
        env['wsgi.input'] = StdIn(req)
        env['wsgi.multiprocess'] = apache.mpm_query(apache.AP_MPMQ_IS_FORKED)
        env['wsgi.multithread'] = apache.mpm_query(apache.AP_MPMQ_IS_THREADED)
        env['wsgi.run_once'] = False
        if env.get('HTTPS') in ('yes', 'on', '1'):
            env['wsgi.url_scheme'] = 'https'
        else:
            env['wsgi.url_scheme'] = 'http'
        env['wsgi.version'] = (1, 0)

    def run(self, application):
        """ run a WSGI application

        @param application WSGI application
        @return None
        """
        try:
            result = application(self.environ, self.start_response)
            for data in result:
                self.write(data)

            if not self.started:
                self.request.set_content_length(0)
            try:
                result.close()
            except (AttributeError,):
                pass

        except:
            import traceback
            traceback.print_exc(None, self.environ['wsgi.errors'])
            if not self.started:
                data = 'A server error occurred. Please contact the administrator.'
                self.request.status = 500
                self.request.content_type = 'text/plain'
                self.request.set_content_length(len(data))
                self.request.write(data)

        return

    def start_response(self, status, headers, exc_info=None):
        """ sets response status, sends response headers

        @param status HTTP status message and code, like '200 OK'
        @param headers sequence of headers as two-tuples
        @return callable for writing response
        """
        if exc_info:
            try:
                if self.started:
                    raise exc_info[0], exc_info[1], exc_info[2]
            finally:
                exc_info = None
        self.request.status = int(status[:3])
        for (key, val) in headers:
            if key.lower() == 'content-length':
                self.request.set_content_length(int(val))
            elif key.lower() == 'content-type':
                self.request.content_type = val
            else:
                self.request.headers_out.add(key, val)

        return self.write

    def write(self, data):
        """ writes response

        @param data value to write to the response
        @return None
        """
        if not self.started:
            self.started = True
        self.request.write(data)


def handler(req):
    """ maps apache/mod_python request to the configured wsgi application

    @param req mod_python request object
    @return always returns apache.OK; HTTP status set by adapter
    """
    (modname, objname) = req.get_options()['wsgi.app'].split('::', 1)
    module = __import__(modname, globals(), locals(), [''])
    app = getattr(module, objname)
    WsgiAdapter(req).run(app)
    return apache.OK