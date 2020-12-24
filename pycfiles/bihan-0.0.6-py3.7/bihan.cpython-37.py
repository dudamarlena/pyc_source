# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\bihan.py
# Compiled at: 2019-06-07 13:56:06
# Size of source mod 2**32: 24992 bytes
"""Minimalist Python web server engine.
Documentation at https://github.com/PierreQuentel/bihan.
"""
import sys, os, re, io, traceback, datetime, cgi, urllib.parse, http.cookies, http.server, email.utils, email.message, json, threading, subprocess, signal, types, wsgiref.simple_server
http_methods = [
 'GET', 'POST', 'DELETE', 'PUT', 'OPTIONS', 'HEAD', 'TRACE',
 'CONNECT']

class HttpRedirection:

    def __init__(self, url):
        self.url = url


class HttpError:

    def __init__(self, code):
        self.code = code


class DispatchError(Exception):
    pass


class RoutingError(Exception):
    pass


class Message:
    __doc__ = 'Generic class for request and response objects'

    def __init__(self):
        self.headers = email.message.Message()
        self.cookies = http.cookies.SimpleCookie()


class Dialog:
    __doc__ = 'Instances of Dialog are passed as arguments to the script functions.\n    They have attributes taken from the application instance.'

    def __init__(self, obj):
        self.environ = obj.env
        self.error = HttpError
        self.redirection = HttpRedirection
        self.request = obj.request
        self.response = obj.response
        self.root = obj.root
        self.routes = obj.routes
        self.template = obj.template


class ImportTracker:
    __doc__ = 'Finder to track all the modules imported by the application'
    _imported = set(['__main__'])
    modules = []
    mtime = {}

    def find_module(self, fullname, path=None):
        self._imported.add(fullname)

    def imported(self):
        """Return all the imported modules (registered or not) in the
        application directory and store their last modification time. Used
        to detect changes and reload the server if necessary.
        """
        if self.modules:
            return (
             self.modules, self.mtime)
        for fullname in self._imported:
            module = sys.modules.get(fullname)
            if module and hasattr(module, '__file__') and module.__file__.startswith(os.getcwd()):
                self.modules.append(module)

        for module in self.modules:
            self.mtime[module.__file__] = os.stat(module.__file__).st_mtime

        return (
         self.modules, self.mtime)


tracker = ImportTracker()
sys.meta_path.insert(0, tracker)

class application(http.server.SimpleHTTPRequestHandler):
    __doc__ = 'WSGI entry point'
    debug = False
    error = None
    registered = []
    root = os.getcwd()
    static = {'/static': os.path.join(os.getcwd(), 'static')}

    def __init__(self, environ, start_response):
        self.env = environ
        self.start_response = start_response
        path = self.env['PATH_INFO']
        if self.env['QUERY_STRING']:
            path += '?' + self.env['QUERY_STRING']
        self.request_version = self.env['SERVER_PROTOCOL']
        self.requestline = '{} {} {}'.format(self.env['REQUEST_METHOD'], path, self.request_version)
        self.client_address = [self.env['REMOTE_ADDR'],
         self.env.get('REMOTE_PORT', self.env['SERVER_PORT'])]
        self.request = request = Message()
        request.url = self.env['PATH_INFO']
        request.method = self.env['REQUEST_METHOD']
        for key in self.env:
            if key == 'HTTP_COOKIE':
                request.cookies = http.cookies.SimpleCookie(self.env[key])
            elif key.startswith('HTTP_'):
                request.headers[key[5:].replace('_', '-')] = self.env[key]
            else:
                if key.upper() == 'CONTENT_LENGTH':
                    request.headers['Content-Length'] = self.env[key]

        self.response = Message()
        self.response.encoding = 'utf-8'
        self.status = '200 Ok'

    def __iter__(self):
        """Iteration expected by the WSGI protocol. Calls start_response
        then yields the response body.
        """
        try:
            self.get_request_fields()
            self.handle()
        except:
            out = io.StringIO()
            traceback.print_exc(file=out)
            self.response.headers.set_type('text/plain')
            self.response.body = out.getvalue().encode(self.response.encoding)

        headers = [(k, str(v)) for k, v in self.response.headers.items()]
        for morsel in self.response.cookies.values():
            headers.append(('Set-Cookie', morsel.output(header='').lstrip()))

        self.start_response(str(self.status), headers)
        yield self.response.body

    @classmethod
    def check_changes(cls):
        """If debug mode is set, check every 2 seconds if one of the source
        files for the imported modules has changed. If so, restart the
        application in a new process.
        """
        modules, mtime = tracker.imported()
        for module in modules:
            if mtime[module.__file__] != os.stat(module.__file__).st_mtime:
                mtime[module.__file__] = os.stat(module.__file__).st_mtime
                python = sys.executable
                args = [
                 python, sys.argv[0], str(os.getpid())]
                subprocess.call(args, shell=True)
                cls.changed = module.__file__

        threading.Timer(2.0, cls.check_changes).start()

    def done(self, code, infile):
        """Send response, cookies, response headers and the data read from
        infile.
        """
        self.status = '{} {}'.format(code, http.server.BaseHTTPRequestHandler.responses[code])
        if code == 500:
            self.response.headers.set_type('text/plain')
        infile.seek(0)
        self.response.body = infile.read()

    def get_request_fields(self):
        """Set self.request.fields, a dictionary indexed by field names.
        If field name ends with [], the value is a list of values.
        Else, it is a single value, or a list if there are several values.
        """
        request = self.request
        request.fields = {}
        fields = urllib.parse.parse_qs((self.env.get('QUERY_STRING', '')), keep_blank_values=1)
        for key in fields:
            if key.endswith('[]'):
                request.fields[key[:-2]] = fields[key]
            elif len(fields[key]) == 1:
                request.fields[key] = fields[key][0]
            else:
                request.fields[key] = fields[key]

        if request.method in ('POST', 'PUT', 'DELETE'):
            charset = 'iso-8859-1'
            for key in request.headers:
                mo = re.search('charset\\s*=(.*)$', request.headers[key])
                if mo:
                    charset = mo.groups()[0]
                    break

            request.encoding = charset
            fp = self.env['wsgi.input']
            has_keys = True
            if 'Content-Type' in request.headers:
                ctype, _ = cgi.parse_header(request.headers['Content-Type'])
                has_keys = ctype == 'application/x-www-form-urlencoded' or ctype.startswith('multipart/')
            if not has_keys:
                length = int(request.headers['Content-Length'])
                request.raw = fp.read(length)

                def _json():
                    return json.loads(request.raw.decode(charset))

                request.json = _json
                return
            body = cgi.FieldStorage(fp, headers=(request.headers), environ={'REQUEST_METHOD': 'POST'})
            data = {}
            for k in body.keys():
                if isinstance(body[k], list):
                    values = [x if x.file else x.value for x in body[k]]
                    if k.endswith('[]'):
                        data[k[:-2]] = values
                    else:
                        data[k] = values
                elif body[k].filename:
                    data[k] = body[k]
                elif k.endswith('[]'):
                    data[k[:-2]] = [
                     body[k].value]
                else:
                    data[k] = body[k].value

            request.fields.update(data)

    @classmethod
    def get_registered(cls):
        """Return the registered modules : those in the main module namespace
        whose source is located in the application directory and don't have
        an attribute __register__ set to False.
        """
        if cls.registered:
            return cls.registered
        main = sys.modules['__main__']
        cls.registered = [main]
        for key in dir(main):
            if key.startswith('_'):
                continue
            obj = getattr(main, key)
            if type(obj) is types.ModuleType and getattr(obj, '__register__', True) and hasattr(obj, '__file__') and obj.__file__.startswith(os.getcwd()):
                cls.registered.append(obj)

        return cls.registered

    def handle(self):
        """Process the data received"""
        if getattr(application, 'changed', False):
            msg = 'Error reloading {}'.format(application.changed)
            return self.done(500, io.BytesIO(msg.encode('utf-8')))
        response = self.response
        self.elts = urllib.parse.urlparse(self.env['PATH_INFO'] + '?' + self.env['QUERY_STRING'])
        self.url = self.elts[2]
        if self.url == '/__doc__':
            doc = []
            for (http_method, pattern), method in application.routes.items():
                doc.append({'http_method':http_method,  'url':pattern[1:-1],  'method':method.__qualname__, 
                 'doc':method.__doc__, 
                 'script':sys.modules[method.__module__].__file__})

            self.response.headers.set_type('application/json')
            res = json.dumps(doc, indent=4)
            return self.done(200, io.BytesIO(res.encode('utf-8')))
        response.headers.set_type('text/html')
        method = self.request.method.lower()
        kind, arg = self.resolve(method, self.url)
        if kind is None:
            if not self.url.endswith('/'):
                kind, arg = self.resolve(method, self.url + '/')
                if kind not in (None, 'file'):
                    self.response.headers['Location'] = self.url + '/'
                    return self.done(302, io.BytesIO())
            return self.send_error(404, 'File not found', 'No route for {} with method {}'.format(self.url, method))
        if kind == 'file':
            if not os.path.exists(arg):
                return self.send_error(404, 'File not found', 'No file matching {}'.format(self.url))
            return self.send_static(arg)
        func, kw = arg
        self.request.fields.update(kw)
        return self.render(func)

    @classmethod
    def load_routes(cls):
        """Build the mapping between url patterns and functions"""
        cls.routes = {}
        for module in cls.get_registered():
            prefix = ''
            if hasattr(module, '__prefix__'):
                prefix = '/' + module.__prefix__.strip('/') + '/'
            classes, functions = [], []
            for key in dir(module):
                obj = getattr(module, key)
                if key.startswith('_'):
                    continue
                if type(obj) is types.FunctionType:
                    if obj.__module__ == module.__name__:
                        functions.append((key, obj))
                if isinstance(obj, type) and obj.__module__ == module.__name__:
                    classes.append((key, obj))

            for key, obj in classes:
                class_urls = getattr(obj, 'urls', [
                 getattr(obj, 'url', key).lstrip('/')])
                for attr in dir(obj):
                    method = getattr(obj, attr)
                    if isinstance(method, types.FunctionType):
                        if not attr.upper() in http_methods:
                            continue
                        method_urls = getattr(method, 'urls', [
                         getattr(method, 'url', None)])
                        if method_urls == [None]:
                            method_urls = class_urls
                        for method_url in method_urls:
                            method_url = '/' + (prefix + method_url).lstrip('/')
                            pattern = re.sub('<(.*?)>', '(?P<\\1>[^/]+?)', method_url)
                            pattern = (
                             attr.lower(), '^' + pattern + '$')
                            if pattern in cls.routes:
                                msg = 'duplicate mapping for "{} {}":\n - in {} line {}\n - in {} line {}'
                                obj2 = cls.routes[pattern]
                                raise RoutingError(msg.format(attr.upper(), method_url, obj2.__code__.co_filename, obj2.__code__.co_firstlineno, method.__code__.co_filename, method.__code__.co_firstlineno))
                            cls.routes[pattern] = method

                        if key.lower() == 'index' and not hasattr(method, 'url'):
                            if (
                             attr.lower(), '^/$') not in cls.routes:
                                cls.routes[(attr.lower(), '^/$')] = method

            for name, function in functions:
                urls = getattr(function, 'urls', [
                 getattr(function, 'url', name)])
                methods = getattr(function, 'methods', ['GET', 'POST'])
                methods = [x.lower() for x in methods]
                for url in urls:
                    url = '/' + (prefix + url).lstrip('/')
                    for method in methods:
                        pattern = re.sub('<(.*?)>', '(?P<\\1>[^/]+?)', url)
                        pattern = (
                         method, '^' + pattern + '$')
                        if pattern in cls.routes:
                            msg = 'duplicate mapping for "{} {}":\n - in {} line {}\n - in {} line {}'
                            obj2 = cls.routes[pattern]
                            raise RoutingError(msg.format(method.upper(), url, obj2.__code__.co_filename, obj2.__code__.co_firstlineno, function.__code__.co_filename, function.__code__.co_firstlineno))
                        cls.routes[pattern] = function
                        if name.lower() == 'index' and not hasattr(function, 'url'):
                            if (
                             method, '^/$') not in cls.routes:
                                cls.routes[(method, '^/$')] = function

    def render(self, func):
        """Run the function and send its result."""
        try:
            result = func(Dialog(self))
            if isinstance(result, HttpRedirection):
                self.response.headers['Location'] = result.url
                return self.done(302, io.BytesIO())
            if isinstance(result, HttpError):
                return self.done(result.code, io.BytesIO())
        except:
            result = io.StringIO()
            if application.debug:
                traceback.print_exc(file=result)
                result = result.getvalue()
            else:
                result = 'Server error'
            return self.send_error(500, 'Server error', result)
        else:
            encoding = self.response.encoding
            if 'charset' not in self.response.headers['Content-Type']:
                if encoding is not None:
                    ctype = self.response.headers['Content-Type']
                    self.response.headers.replace_header('Content-Type', ctype + '; charset={}'.format(encoding))
            else:
                output = io.BytesIO()
                if self.request.method != 'HEAD':
                    if isinstance(result, bytes):
                        output.write(result)
                    else:
                        if isinstance(result, str):
                            try:
                                output.write(result.encode(encoding))
                            except UnicodeEncodeError:
                                msg = io.StringIO()
                                traceback.print_exc(file=msg)
                                return self.done(500, io.BytesIO(msg.getvalue().encode('ascii')))

                        else:
                            output.write(str(result).encode(encoding))
            response_code = getattr(self.response, 'status', 200)
            self.response.headers['Content-Length'] = output.tell()
            self.done(response_code, output)

    def resolve(self, method, url):
        """If url matches a route defined for the application, return the
        tuple ('func', (function_object, arguments)) where function_object is
        the function to call and arguments is a dictionary for smart urls.

        Otherwise, if the url points to a static directory, return the
        tuple ('file', path_in_static_dir).

        Otherwise, return (None, None)
        """
        elts = urllib.parse.unquote(url).lstrip('/').split('/')
        target, patterns = None, []
        for (_method, pattern), obj in application.routes.items():
            if _method != method:
                continue
            mo = re.match(pattern, url, flags=(re.I))
            if mo:
                patterns.append(pattern)
                if target is not None:
                    msg = 'url {} matches at least 2 patterns : {}'
                    raise DispatchError(msg.format(url, patterns))
                target = (
                 obj, mo.groupdict())

        if target is not None:
            return (
             'func', target)
        head = '/' + elts[0]
        if head in self.static:
            return (
             'file', (os.path.join)(self.static[head], *elts[1:]))
        return (None, None)

    @classmethod
    def run(cls, host='localhost', port=8000, debug=False):
        """Start the built-in server"""
        cls.httpd = wsgiref.simple_server.make_server(host, port, application)
        print('Serving on port {}'.format(port))
        if len(sys.argv) > 1:
            pid = sys.argv[1]
            os.kill(int(pid), signal.SIGTERM)
        cls.load_routes()
        if debug not in (True, False):
            raise ValueError('debug must be True or False')
        cls.debug = debug
        if cls.debug:
            cls.check_changes()
        cls.httpd.serve_forever()

    def send_error(self, code, expl, msg=''):
        """Send an error message"""
        self.status = '{} {}'.format(code, expl)
        self.response.headers.set_type('text/plain')
        if not self.debug:
            msg = expl
        self.response.body = msg.encode(self.response.encoding)

    def send_static(self, fs_path):
        """Send the content of a file"""
        try:
            f = open(fs_path, 'rb')
            fs = os.fstat(f.fileno())
        except IOError:
            return self.send_error(404, 'File not found', 'No file found for given url')
        else:
            if 'If-Modified-Since' in self.request.headers:
                try:
                    ims = email.utils.parsedate_to_datetime(self.request.headers['If-Modified-Since'])
                except (TypeError, IndexError, OverflowError, ValueError):
                    pass
                else:
                    if ims.tzinfo is None:
                        ims = ims.replace(tzinfo=(datetime.timezone.utc))
                    if ims.tzinfo is datetime.timezone.utc:
                        last_modif = datetime.datetime.fromtimestamp(fs.st_mtime, datetime.timezone.utc)
                        last_modif = last_modif.replace(microsecond=0)
                        if last_modif <= ims:
                            f.close()
                            return self.done(304, io.BytesIO())
            ctype = self.guess_type(fs_path)
            if ctype.startswith('text/'):
                ctype += ';charset=utf-8'
            self.response.headers.set_type(ctype)
            self.response.headers['Last-Modified'] = self.date_time_string(fs.st_mtime)
            self.response.headers['Content-Length'] = str(os.fstat(f.fileno())[6])
            self.done(200, f)

    def template(self, filename, **kw):
        """If the template engine patrom is installed, use it to render the
        template file with the specified key/values.
        """
        from patrom import TemplateParser, TemplateError
        parser = TemplateParser()
        path = os.path.join(application.root, 'templates', filename)
        try:
            result = (parser.render)(path, **kw)
            self.response.headers.set_type('text/html')
        except TemplateError as exc:
            try:
                result = str(exc)
                self.response.headers.set_type('text/plain')
            finally:
                exc = None
                del exc

        return result


if __name__ == '__main__':
    application.run(port=8000)