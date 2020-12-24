# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyojo\__init__.py
# Compiled at: 2013-06-09 17:34:09
__doc__ = ' This is the main pyojo module. \n\n    The goal is to define a page with modular building blocks witch will be \n    asynchronously loaded from the server, who will send the javascript code \n    to create them at the browser. If a block depends on the previous existence\n    of another block (its parent, for example), the pyojo script will try to \n    retrieve all dependencies before executing the code.\n    \n    Request is the entry point, create a instance passing environ and then use\n    the get_response() to get the content. The get_headers() method and the \n    status attribute are then passed to the WSGI start_response function.\n    \n    The response must be iterable, and there is a collection of ContentType\n    subclasses that can be returned to the WSGI applicattion depending on the\n    type of the response, they return the iterable when called.\n    \n    There is one special ContentType subclass called Reply, witch handles the\n    Response subclass responses, to do your own custom responses.\n                \n'
__author__ = 'Txema Vicente Segura'
__version__ = '0.0.2 prealpha'
__copyright__ = 'Copyright (C) 2013 nabla.net'
import time, rfc822, traceback, pyojo.data as data, pyojo.content as content
from .func import *
from .base import *

class Request(object):
    """ Answers a request with an appropriate response.
    
        The WSGI application creates one instance and then asks 
        a response calling the get_response method.
        
    """

    def __init__(self, environ=None):
        """ Create an instance to find the response for a request.
        
            :param environ: 
               request description, as described in 
               http://www.python.org/dev/peps/pep-0333/
            
            :type environ: dict
            
            Attributes:
            
             - **environ**:  Request description.
             - **url**: HTTP path.
             - **method**: HTTP verb.
             - **query**: Request parameters
             - **accept**: Expected content type.
             - **async**: True if AJAX.
             - **cookies**: Cookies.
             - **response_header**: Response Headers.
              
             
        """
        self.environ = environ
        self.response = None
        self._status = 102
        self.handler_info = 'None'
        self.error_info = ''
        self.response_header = data.LimitedDict(data.HEADERS_RESPONSE)
        self.response_header['Server'] = 'pyojo %s' % __version__
        self.response_header['Date'] = rfc822.formatdate(time.time())
        if environ is None:
            self.config = None
            self.environ = {}
            self.url = '/'
            self.method = None
            self.query = ()
            self.accept = '*/*'
            self.async = False
            self.cookies = ''
        else:
            self.init(environ)
        return

    def __call__(self, environ, start_response):
        """ Act like a WSGI application.
        
            :param start_response:
                If passed, then .
               
        """
        response = self.get_response()
        start_response(self.status, self.get_response_headers())
        return response

    def init(self, environ):
        """ Initialize attributes analyzing environ.
            
            :param environ: request description dictionary.
        """
        self.environ = environ
        self.url = environ['PATH_INFO']
        self.method = environ['REQUEST_METHOD']
        self.query = parse_qs(environ['QUERY_STRING'])
        self.accept = environ.get('HTTP_ACCEPT', '*/*')
        if '/dojo/' not in self.url:
            log.debug('Request %s %s %s', self.url, self.method, self.accept.split(';')[0])
        requested_with = environ.get('HTTP_X_REQUESTED_WITH')
        self.async = 'XMLHttpRequest' == requested_with
        self.cookies = environ.get('HTTP_COOKIE', '')
        self.route_type = {'function': self.route_function, 'class': self.route_class}
        try:
            self.config = Config
        except NameError:

            class Temp(object):
                """Mock Config"""
                www = None
                url = None
                route = []
                debug = True

            self.config = Temp

    def __deduce(self):
        """ Find the answer.
        
            Checks routes and static files, looking for the correct answer.
            
            :returns: something or None
        """
        if content.CachedText.instances.has_key(self.url):
            return content.CachedText(self.url)
        else:
            if '/static/' in self.url:
                sequence = (
                 self.static, self.route, self.module)
            else:
                sequence = (
                 self.module, self.route, self.static)
            for method in sequence:
                response = method()
                if response is not None:
                    return response

            return

    def get_response(self):
        """ Get the response.
        
            :returns: the response
            :rtype: iterable
        """
        handler = None
        response = self.__deduce()
        if True:
            if self.async:
                handler_info = 'XHR-' + self.handler_info
            else:
                handler_info = self.handler_info
            self.response_header['X-Handler'] = handler_info
            self.response_header['X-Type'] = str(type(response))[1:-1]
        if isinstance(response, ContentType):
            self._log_content(response)
            handler = response
        else:
            rtype = type(response).__name__
            for cls in subclasses(ContentType):
                if cls.handles(response):
                    handler = cls(response)
                    self._log_content(handler, rtype)
                    break

        if handler is not None:
            if self.param('code') is not None:
                print 'SEE %s' % type(handler)
                return handler.see(self)
            else:
                return handler(self)

        log.warning('Response type %s unknown', type(response))
        if self.status == 102:
            self.status = 501
        return response

    def get_response_headers(self):
        """ Get headers as a list of tuples.
        """
        if self.response_header['Content-Type'] is None:
            log.warn('Content-Type header is not set for %s', self.url)
        response_headers = []
        for key, value in self.response_header.iteritems():
            response_headers.append((key, str(value)))

        return response_headers

    @property
    def status(self):
        """ Get the current status code.
        
            :returns: status code and description
            :rtype: string
        """
        status = '%s %s' % (self._status, data.HTTP_STATUS[self._status])
        return status

    @status.setter
    def status--- This code section failed: ---

 L. 246         0  LOAD_FAST             1  'code'
                3  LOAD_GLOBAL           0  'data'
                6  LOAD_ATTR             1  'HTTP_STATUS'
                9  LOAD_ATTR             2  'keys'
               12  CALL_FUNCTION_0       0  None
               15  COMPARE_OP            6  in
               18  POP_JUMP_IF_TRUE     30  'to 30'
               21  LOAD_ASSERT              AssertionError
               24  LOAD_CONST               'HTTP Status unknown'
               27  RAISE_VARARGS_2       2  None

 L. 247        30  LOAD_FAST             1  'code'
               33  LOAD_FAST             0  'self'
               36  STORE_ATTR            4  '_status'

 L. 248        39  LOAD_FAST             1  'code'
               42  LOAD_CONST               200
               45  COMPARE_OP            3  !=
               48  POP_JUMP_IF_FALSE    76  'to 76'

 L. 249        51  LOAD_GLOBAL           5  'log'
               54  LOAD_ATTR             6  'debug'
               57  LOAD_CONST               'HTTP Status %s for %s'
               60  LOAD_FAST             1  'code'
               63  LOAD_FAST             0  'self'
               66  LOAD_ATTR             7  'url'
               69  CALL_FUNCTION_3       3  None
               72  POP_TOP          
               73  JUMP_FORWARD          0  'to 76'
             76_0  COME_FROM            73  '73'

Parse error at or near `JUMP_FORWARD' instruction at offset 73

    def content_type(self, mime):
        """ Sets the content type, and charset if applicable.
        """
        if 'text' in mime and 'charset' not in mime:
            mime += '; charset=utf-8'
        self.response_header['Content-Type'] = mime

    def static(self, url=None):
        """ Look for a static file.
        
            :returns: FileSystem or CachedText instance, or None.
        """
        if url is None:
            url = self.url
        if self.config.www is None:
            log.error('Static files folder not configured')
            return
        else:
            path = url.replace('/', os.path.sep)
            if path.startswith(os.path.sep):
                path = path[1:]
            filename = os.path.normpath(os.path.join(self.config.www, path))
            if not os.path.isfile(filename):
                return
            ext = os.path.splitext(path)[1][1:]
            if not data.MIMETYPE.has_key(ext):
                log.error("Unknown mimetype for '%s'", ext)
                return
            if ext in ('js', 'css', 'html'):
                return content.CachedText(url, filename)
            return content.FileSystem(filename)

    def module(self, url=None):
        """ Look for a python module.
        
            :returns: result of calling the HTTP verb, or None.
        """
        if self.config.url is None:
            return
        else:
            if url is None:
                url = self.url
            mod_name = ('_').join(url.lstrip('/').rsplit('.', 1))
            path_mod = os.path.abspath(os.path.join(Config.url, mod_name + '.py'))
            if not os.path.exists(path_mod):
                return
            self.handler_info = 'module %s' % mod_name
            try:
                module = import_url(Config.url, url)
            except ModuleNotFoundError as ex:
                log.warning('Module %s: %s', mod_name, ex)
                return
            except Exception as ex:
                log.error('Exception loading %s: %s', mod_name, ex)
                return self.error(sys.exc_info())

            if module is None:
                return
            ext = os.path.splitext(url)[1]
            if len(ext) > 0:
                self.content_type(data.MIMETYPE[ext[1:]])
            function = self.method
            if self.param('method') is not None:
                function = self.param('method')
            self.handler_info = 'module %s.%s' % (mod_name, function)
            if hasattr(module, function):
                call = getattr(module, function)
                try:
                    response = call(self)
                except Exception as ex:
                    log.error('Exception calling %s.%s: %s', mod_name, function, ex)
                    return self.error(sys.exc_info())

                self.status = 200
                return response
            return

    def route_function(self, routeobj, params=None):
        """ Call the route function.
        
            Check expected arguments and call the handler function.
        """
        if params is None:
            params = {}
        kwargs = params
        if 'request' in routeobj.args:
            kwargs['request'] = self
        if 'environ' in routeobj.args:
            kwargs['environ'] = self.environ
        self.handler_info = 'function %s(%s)' % (routeobj.name,
         repr(kwargs)[1:-1])
        log.debug("Route '%s' is '%s': %s %s (%s) type '%s' for '%s'", self.url, routeobj.route, routeobj.type, routeobj.name, kwargs, routeobj.accept, self.accept)
        try:
            response = routeobj.call(**kwargs)
        except Exception:
            return self.error(sys.exc_info())

        return response

    def route_class(self, routeobj, params=None):
        """ Call the route class.
        
            If is a Response subclass, create a new instance. Then the route 
            parameters are set as instance attributes, and the requested method 
            is called.
            
            TODO: params, other classes
        """
        if params is None:
            params = {}
        if issubclass(routeobj.call, Reply):
            self.handler_info = 'class %s(%s).%s %s' % (routeobj.name,
             id(self),
             self.method,
             params)
            obj = routeobj.call(self)
            self.content_type(obj.content)
            for attr, value in params.iteritems():
                setattr(obj, attr, value)

            try:
                method = getattr(obj, self.method)
                response = method()
            except Exception:
                return self.error(sys.exc_info())

            return response
        return

    def route(self):
        """ Look for a appropiate route.
        
            Checks the route map and if one route accepts the URL and the request
            method, and it fits in the expected Content-Type, calls the route and
            returns the returned value.
        
            :returns: route call result 
            :rtype: something or None
        """
        for route in self.config.route:
            match = route.regex.match(self.url)
            if match:
                if self.method not in route.method:
                    continue
                if not accepts(route.accept, self.accept):
                    continue
                self.status = 200
                return self.route_type[route.type](route, match.groupdict())

        return

    def error(self, exc_info):
        """ Handles exceptions.
        
            :returns: Traceback
        """
        exc_type, exc_value, exc_traceback = exc_info
        status = 'Request %s%s %s accepts %s' % ('XHR-' if self.async else '',
         self.method,
         self.url,
         self.accept)
        status += '\nHandler %s' % self.handler_info
        error = '%s: %s' % (exc_type.__name__, exc_value)
        trace = '\n'
        for line in traceback.format_tb(exc_traceback):
            trace += '%s\n' % line

        print status + trace + error
        self.error_info = status + trace + error
        self.status = 500
        return Traceback(exc_info, self)

    def param(self, param):
        """ Get a query parameter value.
        
            :param param: parameter name
            :type param: string
            :returns: value
            :rtype: string
        """
        value = self.query.get(param, None)
        if type(value) == type([]):
            if len(value) == 1:
                return value[0]
        return value

    def _log_content(self, response, rtype=None):
        """ Log content type.
        """
        if '/dojo/' in self.url:
            return
        else:
            if '/favicon' in self.url:
                return
            if rtype is None:
                rtype = response.rtype()
            else:
                rtype = '*' + rtype
            log.debug('Content %s(%s) %s %s', response.__class__.__name__, rtype, self.response_header['Content-Type'], self.status)
            return