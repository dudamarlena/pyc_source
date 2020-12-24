# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pycoon\wsgi\servers\paste\modpython.py
# Compiled at: 2006-12-06 18:47:32
"""WSGI Paste wrapper for mod_python. Requires Python 2.2 or greater.

Example httpd.conf section for a Paste app with an ini file::

    <Location />
        SetHandler python-program
        PythonHandler paste.modpython
        PythonOption paste.ini /some/location/your/pasteconfig.ini
    </Location>
    
Or if you want to load a WSGI application under /your/homedir in the module
``startup`` and the WSGI app is ``app``::

    <Location />
        SetHandler python-program
        PythonHandler paste.modpython
        PythonPath "['/virtual/project/directory'] + sys.path"
        PythonOption wsgi.application startup::app
    </Location>

If you'd like to use a virtual installation, make sure to add it in the path
like so::

    <Location />
        SetHandler python-program
        PythonHandler paste.modpython
        PythonPath "['/virtual/project/directory', '/virtual/lib/python2.4/'] + sys.path"
        PythonOption paste.ini /virtual/project/directory/pasteconfig.ini
    </Location>

Some WSGI implementations assume that the SCRIPT_NAME environ variable will
always be equal to "the root URL of the app"; Apache probably won't act as
you expect in that case. You can add another PythonOption directive to tell
modpython_gateway to force that behavior:

    PythonOption SCRIPT_NAME /mcontrol

Some WSGI applications need to be cleaned up when Apache exits. You can
register a cleanup handler with yet another PythonOption directive:

    PythonOption wsgi.cleanup module::function

The module.function will be called with no arguments on server shutdown,
once for each child process or thread.

This module highly based on Robert Brewer's, here:
http://projects.amor.org/misc/svn/modpython_gateway.py
"""
import traceback
try:
    from mod_python import apache
except:
    pass

class InputWrapper(object):
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


class ErrorWrapper(object):
    __module__ = __name__

    def __init__(self, req):
        self.req = req

    def flush(self):
        pass

    def write(self, msg):
        self.req.log_error(msg)

    def writelines(self, seq):
        self.write(('').join(seq))


bad_value = "You must provide a PythonOption '%s', either 'on' or 'off', when running a version of mod_python < 3.1"

class Handler:
    __module__ = __name__

    def __init__(self, req):
        self.started = False
        options = req.get_options()
        try:
            q = apache.mpm_query
            threaded = q(apache.AP_MPMQ_IS_THREADED)
            forked = q(apache.AP_MPMQ_IS_FORKED)
        except AttributeError:
            threaded = options.get('multithread', '').lower()
            if threaded == 'on':
                threaded = True
            elif threaded == 'off':
                threaded = False
            else:
                raise ValueError(bad_value % 'multithread')
            forked = options.get('multiprocess', '').lower()
            if forked == 'on':
                forked = True
            elif forked == 'off':
                forked = False
            else:
                raise ValueError(bad_value % 'multiprocess')

        env = self.environ = dict(apache.build_cgi_env(req))
        if 'SCRIPT_NAME' in options:
            env['SCRIPT_NAME'] = options['SCRIPT_NAME']
            env['PATH_INFO'] = req.uri[len(options['SCRIPT_NAME']):]
        else:
            env['SCRIPT_NAME'] = ''
            env['PATH_INFO'] = req.uri
        env['wsgi.input'] = InputWrapper(req)
        env['wsgi.errors'] = ErrorWrapper(req)
        env['wsgi.version'] = (1, 0)
        env['wsgi.run_once'] = False
        if env.get('HTTPS') in ('yes', 'on', '1'):
            env['wsgi.url_scheme'] = 'https'
        else:
            env['wsgi.url_scheme'] = 'http'
        env['wsgi.multithread'] = threaded
        env['wsgi.multiprocess'] = forked
        self.request = req

    def run(self, application):
        try:
            result = application(self.environ, self.start_response)
            for data in result:
                self.write(data)

            if not self.started:
                self.request.set_content_length(0)
            if hasattr(result, 'close'):
                result.close()
        except:
            traceback.print_exc(None, self.environ['wsgi.errors'])
            if not self.started:
                self.request.status = 500
                self.request.content_type = 'text/plain'
                data = 'A server error occurred. Please contact the administrator.'
                self.request.set_content_length(len(data))
                self.request.write(data)

        return

    def start_response(self, status, headers, exc_info=None):
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
        if not self.started:
            self.started = True
        self.request.write(data)


startup = None
cleanup = None
wsgiapps = {}

def handler(req):
    global cleanup
    global startup
    global wsgiapps
    options = req.get_options()
    if 'wsgi.startup' in options and not startup:
        func = options['wsgi.startup']
        if func:
            (module_name, object_str) = func.split('::', 1)
            module = __import__(module_name, globals(), locals(), [''])
            startup = apache.resolve_object(module, object_str)
            startup(req)
    if 'wsgi.cleanup' in options and not cleanup:
        func = options['wsgi.cleanup']
        if func:
            (module_name, object_str) = func.split('::', 1)
            module = __import__(module_name, globals(), locals(), [''])
            cleanup = apache.resolve_object(module, object_str)

            def cleaner(data):
                cleanup()

            try:
                apache.register_cleanup(cleaner)
            except AttributeError:
                req.server.register_cleanup(req, cleaner)

    appini = options.get('paste.ini')
    app = None
    if appini:
        if appini not in wsgiapps:
            wsgiapps[appini] = loadapp('config:%s' % appini)
        app = wsgiapps[appini]
    appwsgi = options.get('wsgi.application')
    if appwsgi and not appini:
        (modname, objname) = appwsgi.split('::', 1)
        module = __import__(modname, globals(), locals(), [''])
        app = getattr(module, objname)
    Handler(req).run(app)
    return apache.OK