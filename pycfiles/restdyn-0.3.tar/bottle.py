# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/namlook/Documents/projects/restdyn/tests/bottle.py
# Compiled at: 2011-09-02 10:25:26
"""
Bottle is a fast and simple micro-framework for small web applications. It
offers request dispatching (Routes) with url parameter support, templates,
a built-in HTTP Server and adapters for many third party WSGI/HTTP-server and
template engines - all in a single file and with no dependencies other than the
Python Standard Library.

Homepage and documentation: http://bottlepy.org/

Copyright (c) 2011, Marcel Hellkamp.
License: MIT (see LICENSE.txt for details)
"""
from __future__ import with_statement
__author__ = 'Marcel Hellkamp'
__version__ = '0.10.dev'
__license__ = 'MIT'
import base64, cgi, email.utils, functools, hmac, httplib, imp, itertools, mimetypes, os, re, subprocess, sys, tempfile, thread, threading, time, warnings
from Cookie import SimpleCookie
from tempfile import TemporaryFile
from traceback import format_exc
from urlparse import urljoin, SplitResult as UrlSplitResult
from types import MethodType
import urllib
urlencode = urllib.urlencode
urlquote = urllib.quote
urlunquote = urllib.unquote
try:
    from collections import MutableMapping as DictMixin
except ImportError:
    from UserDict import DictMixin

try:
    from urlparse import parse_qs
except ImportError:
    from cgi import parse_qs

try:
    import cPickle as pickle
except ImportError:
    import pickle

try:
    from json import dumps as json_dumps, loads as json_lds
except ImportError:
    try:
        from simplejson import dumps as json_dumps, loads as json_lds
    except ImportError:
        try:
            from django.utils.simplejson import dumps as json_dumps, loads as json_lds
        except ImportError:

            def json_dumps(data):
                raise ImportError('JSON support requires Python 2.6 or simplejson.')


            json_lds = json_dumps

py3k = sys.version_info >= (3, 0, 0)
NCTextIOWrapper = None
if py3k:
    json_loads = lambda s: json_lds(touni(s))
    from io import BytesIO

    def touni(x, enc='utf8', err='strict'):
        """ Convert anything to unicode """
        if isinstance(x, bytes):
            return str(x, enc, err)
        return str(x)


    if sys.version_info < (3, 2, 0):
        from io import TextIOWrapper

        class NCTextIOWrapper(TextIOWrapper):
            """ Garbage collecting an io.TextIOWrapper(buffer) instance closes
                the wrapped buffer. This subclass keeps it open. """

            def close(self):
                pass


else:
    json_loads = json_lds
    from StringIO import StringIO as BytesIO
    bytes = str

    def touni(x, enc='utf8', err='strict'):
        """ Convert anything to unicode """
        if isinstance(x, unicode):
            return x
        return unicode(str(x), enc, err)


def tob(data, enc='utf8'):
    """ Convert anything to bytes """
    if isinstance(data, unicode):
        return data.encode(enc)
    return bytes(data)


if py3k:
    tonat = touni
else:
    tonat = tob
tonat.__doc__ = ' Convert anything to native strings '

def depr(message, critical=False):
    if critical:
        raise DeprecationWarning(message)
    warnings.warn(message, DeprecationWarning, stacklevel=3)


def makelist(data):
    if isinstance(data, (tuple, list, set, dict)):
        return list(data)
    else:
        if data:
            return [data]
        return []


class DictProperty(object):
    """ Property that maps to a key in a local dict-like attribute. """

    def __init__(self, attr, key=None, read_only=False):
        self.attr, self.key, self.read_only = attr, key, read_only

    def __call__(self, func):
        functools.update_wrapper(self, func, updated=[])
        self.getter, self.key = func, self.key or func.__name__
        return self

    def __get__(self, obj, cls):
        if obj is None:
            return self
        else:
            key, storage = self.key, getattr(obj, self.attr)
            if key not in storage:
                storage[key] = self.getter(obj)
            return storage[key]

    def __set__(self, obj, value):
        if self.read_only:
            raise AttributeError('Read-Only property.')
        getattr(obj, self.attr)[self.key] = value

    def __delete__(self, obj):
        if self.read_only:
            raise AttributeError('Read-Only property.')
        del getattr(obj, self.attr)[self.key]


class CachedProperty(object):
    """ A property that is only computed once per instance and then replaces
        itself with an ordinary attribute. Deleting the attribute resets the
        property. """

    def __init__(self, func):
        self.func = func

    def __get__(self, obj, cls):
        if obj is None:
            return self
        else:
            value = obj.__dict__[self.func.__name__] = self.func(obj)
            return value


cached_property = CachedProperty

class lazy_attribute(object):
    """ A property that caches itself to the class object. """

    def __init__(self, func):
        functools.update_wrapper(self, func, updated=[])
        self.getter = func

    def __get__(self, obj, cls):
        value = self.getter(cls)
        setattr(cls, self.__name__, value)
        return value


class BottleException(Exception):
    """ A base class for exceptions used by bottle. """
    pass


class HTTPResponse(BottleException):
    """ Used to break execution and immediately finish the response """

    def __init__(self, output='', status=200, header=None):
        super(BottleException, self).__init__('HTTP Response %d' % status)
        self.status = int(status)
        self.output = output
        self.headers = HeaderDict(header) if header else None
        return

    def apply(self, response):
        if self.headers:
            for (key, value) in self.headers.iterallitems():
                response.headers[key] = value

        response.status = self.status


class HTTPError(HTTPResponse):
    """ Used to generate an error page """

    def __init__(self, code=500, output='Unknown Error', exception=None, traceback=None, header=None):
        super(HTTPError, self).__init__(output, code, header)
        self.exception = exception
        self.traceback = traceback

    def __repr__(self):
        return template(ERROR_PAGE_TEMPLATE, e=self)


class RouteError(BottleException):
    """ This is a base class for all routing related exceptions """
    pass


class RouteReset(BottleException):
    """ If raised by a plugin or request handler, the route is reset and all
        plugins are re-applied. """
    pass


class RouteSyntaxError(RouteError):
    """ The route parser found something not supported by this router """
    pass


class RouteBuildError(RouteError):
    """ The route could not been built """
    pass


class Router(object):
    """ A Router is an ordered collection of route->target pairs. It is used to
        efficiently match WSGI requests against a number of routes and return
        the first target that satisfies the request. The target may be anything,
        usually a string, ID or callable object. A route consists of a path-rule
        and a HTTP method.

        The path-rule is either a static path (e.g. `/contact`) or a dynamic
        path that contains wildcards (e.g. `/wiki/:page`). By default, wildcards
        consume characters up to the next slash (`/`). To change that, you may
        add a regular expression pattern (e.g. `/wiki/:page#[a-z]+#`).

        For performance reasons, static routes (rules without wildcards) are
        checked first. Dynamic routes are searched in order. Try to avoid
        ambiguous or overlapping rules.

        The HTTP method string matches only on equality, with two exceptions:
          * ´GET´ routes also match ´HEAD´ requests if there is no appropriate
            ´HEAD´ route installed.
          * ´ANY´ routes do match if there is no other suitable route installed.

        An optional ``name`` parameter is used by :meth:`build` to identify
        routes.
    """
    default = '[^/]+'

    @lazy_attribute
    def syntax(cls):
        return re.compile('(?<!\\\\):([a-zA-Z_][a-zA-Z_0-9]*)?(?:#(.*?)#)?')

    def __init__(self):
        self.routes = {}
        self.rules = []
        self.named = {}
        self.static = {}
        self.dynamic = []

    def add(self, rule, method, target, name=None):
        """ Add a new route or replace the target for an existing route. """
        if rule in self.routes:
            self.routes[rule][method.upper()] = target
        else:
            self.routes[rule] = {method.upper(): target}
            self.rules.append(rule)
            if self.static or self.dynamic:
                self.static, self.dynamic = {}, {}
        if name:
            self.named[name] = (
             rule, None)
        return

    def build(self, _name, *anon, **args):
        """ Return a string that matches a named route. Use keyword arguments
            to fill out named wildcards. Remaining arguments are appended as a
            query string. Raises RouteBuildError or KeyError."""
        if _name not in self.named:
            raise RouteBuildError('No route with that name.', _name)
        (rule, pairs) = self.named[_name]
        if not pairs:
            token = self.syntax.split(rule)
            parts = [ p.replace('\\:', ':') for p in token[::3] ]
            names = token[1::3]
            if len(parts) > len(names):
                names.append(None)
            pairs = zip(parts, names)
            self.named[_name] = (rule, pairs)
        try:
            anon = list(anon)
            url = [ s if k is None else s + str(args.pop(k)) if k else (s + str(anon.pop())) for (s, k) in pairs
                  ]
        except IndexError:
            msg = 'Not enough arguments to fill out anonymous wildcards.'
            raise RouteBuildError(msg)
        except KeyError, e:
            raise RouteBuildError(*e.args)

        if args:
            url += ['?', urlencode(args)]
        return ('').join(url)

    def match(self, environ):
        """ Return a (target, url_agrs) tuple or raise HTTPError(404/405). """
        (targets, urlargs) = self._match_path(environ)
        if not targets:
            raise HTTPError(404, 'Not found: ' + repr(environ['PATH_INFO']))
        method = environ['REQUEST_METHOD'].upper()
        if method in targets:
            return (targets[method], urlargs)
        if method == 'HEAD' and 'GET' in targets:
            return (targets['GET'], urlargs)
        if 'ANY' in targets:
            return (targets['ANY'], urlargs)
        allowed = [ verb for verb in targets if verb != 'ANY' ]
        if 'GET' in allowed and 'HEAD' not in allowed:
            allowed.append('HEAD')
        raise HTTPError(405, 'Method not allowed.', header=[
         (
          'Allow', (',').join(allowed))])

    def _match_path(self, environ):
        """ Optimized PATH_INFO matcher. """
        path = environ['PATH_INFO'] or '/'
        match = self.static.get(path)
        if match:
            return (match, {})
        else:
            for (combined, rules) in self.dynamic:
                match = combined.match(path)
                if not match:
                    continue
                (gpat, match) = rules[(match.lastindex - 1)]
                return (match, gpat(path).groupdict() if gpat else {})

            if self.static or self.dynamic or not self.routes:
                return (None, {})
            if not environ.get('wsgi.run_once'):
                self._compile()
                return self._match_path(environ)
            epath = path.replace(':', '\\:')
            match = self.routes.get(epath)
            if match:
                return (match, {})
            for rule in self.rules:
                if rule.count(':') < rule.count('\\:'):
                    continue
                match = self._compile_pattern(rule).match(path)
                if match:
                    return (self.routes[rule], match.groupdict())

            return (
             None, {})

    def _compile(self):
        """ Prepare static and dynamic search structures. """
        self.static = {}
        self.dynamic = []

        def fpat_sub(m):
            if len(m.group(1)) % 2:
                return m.group(0)
            return m.group(1) + '(?:'

        for rule in self.rules:
            target = self.routes[rule]
            if not self.syntax.search(rule):
                self.static[rule.replace('\\:', ':')] = target
                continue
            gpat = self._compile_pattern(rule)
            fpat = re.sub('(\\\\*)(\\(\\?P<[^>]*>|\\((?!\\?))', fpat_sub, gpat.pattern)
            gpat = gpat.match if gpat.groupindex else None
            try:
                combined = '%s|(%s)' % (self.dynamic[(-1)][0].pattern, fpat)
                self.dynamic[-1] = (re.compile(combined), self.dynamic[(-1)][1])
                self.dynamic[(-1)][1].append((gpat, target))
            except (AssertionError, IndexError), e:
                self.dynamic.append((re.compile('(^%s$)' % fpat),
                 [
                  (
                   gpat, target)]))
            except re.error, e:
                raise RouteSyntaxError('Could not add Route: %s (%s)' % (rule, e))

        return

    def _compile_pattern(self, rule):
        """ Return a regular expression with named groups for each wildcard. """
        out = ''
        for (i, part) in enumerate(self.syntax.split(rule)):
            if i % 3 == 0:
                out += re.escape(part.replace('\\:', ':'))
            elif i % 3 == 1:
                out += '(?P<%s>' % part if part else '(?:'
            else:
                out += '%s)' % (part or '[^/]+')

        return re.compile('^%s$' % out)


class Route(object):
    """ This class wraps a route callback along with route specific metadata and
        configuration and applies Plugins on demand. """

    def __init__(self, app, rule, method, callback, name=None, plugins=None, skiplist=None, **config):
        self.app = app
        self.rule = rule
        self.method = method
        self.callback = callback
        self.name = name or None
        self.plugins = plugins or []
        self.skiplist = skiplist or []
        self.config = config
        return

    def __call__(self, *a, **ka):
        depr('Some APIs changed to return Route() instances instead of callables. Make sure to use the Route.call method and not to call Route instances directly.')
        return self.call(*a, **ka)

    @cached_property
    def call(self):
        """ The route callback with all plugins applied. This property is
            created on demand and then cached to speed ub subsequent requests."""
        return self._make_callback()

    def reset(self):
        """ Forget any cached values. The next time :attr:`call` is accessed,
            all plugins are re-applied. """
        self.__dict__.pop('call', None)
        return

    def prepare(self):
        """ Do all on-demand work immediately (useful for debugging)."""
        self.call

    @property
    def _context(self):
        depr('Switch to Plugin API v2 and access the Route object directly.')
        return dict(rule=self.rule, method=self.method, callback=self.callback, name=self.name, app=self.app, config=self.config, apply=self.plugins, skip=self.skiplist)

    def all_plugins(self):
        """ Return a list of all Plugins that affect this route. """
        if True in self.skiplist:
            return []
        return [ p for p in reversed(self.app.plugins + self.plugins) if p not in self.skiplist if type(p) not in self.skiplist if getattr(p, 'name', True) not in self.skiplist ]

    def _make_callback(self):
        callback = self.callback
        for plugin in self.all_plugins():
            try:
                if hasattr(plugin, 'apply'):
                    api = getattr(plugin, 'api', 1)
                    context = self if api > 1 else self._context
                    callback = plugin.apply(callback, context)
                else:
                    callback = plugin(callback)
            except RouteReset:
                return self._make_callback()
            else:
                functools.update_wrapper(callback, self.callback)

        return callback


class Bottle(object):
    """ WSGI application """

    def __init__(self, catchall=True, autojson=True, config=None):
        """ Create a new bottle instance.
            You usually don't do that. Use `bottle.app.push()` instead.
        """
        self.routes = []
        self.router = Router()
        self.plugins = []
        self.mounts = {}
        self.error_handler = {}
        self.catchall = catchall
        self.config = config or {}
        self.hooks = self.install(HooksPlugin())
        if autojson:
            self.install(JSONPlugin())
        self.install(TemplatePlugin())

    def mount(self, app, prefix, **options):
        """ Mount an application to a specific URL prefix. The prefix is added
            to SCIPT_PATH and removed from PATH_INFO before the sub-application
            is called.

            :param app: an instance of :class:`Bottle`.
            :param prefix: path prefix used as a mount-point.

            All other parameters are passed to the underlying :meth:`route` call.
        """
        if not isinstance(app, Bottle):
            raise TypeError('Only Bottle instances are supported for now.')
        prefix = ('/').join(filter(None, prefix.split('/')))
        if not prefix:
            raise TypeError('Empty prefix. Perhaps you want a merge()?')
        for other in self.mounts:
            if other.startswith(prefix):
                raise TypeError('Conflict with existing mount: %s' % other)

        path_depth = prefix.count('/') + 1
        options.setdefault('method', 'ANY')
        options.setdefault('skip', True)
        self.mounts[prefix] = app

        @self.route(('/%s/:#.*#' % prefix), **options)
        def mountpoint():
            request.path_shift(path_depth)
            return app._handle(request.environ)

        return

    def install(self, plugin):
        """ Add a plugin to the list of plugins and prepare it for being
            applied to all routes of this application. A plugin may be a simple
            decorator or an object that implements the :class:`Plugin` API.
        """
        if hasattr(plugin, 'setup'):
            plugin.setup(self)
        if not callable(plugin) and not hasattr(plugin, 'apply'):
            raise TypeError('Plugins must be callable or implement .apply()')
        self.plugins.append(plugin)
        self.reset()
        return plugin

    def uninstall(self, plugin):
        """ Uninstall plugins. Pass an instance to remove a specific plugin, a type
            object to remove all plugins that match that type, a string to remove
            all plugins with a matching ``name`` attribute or ``True`` to remove all
            plugins. Return the list of removed plugins. """
        removed, remove = [], plugin
        for (i, plugin) in list(enumerate(self.plugins))[::-1]:
            if remove is True or remove is plugin or remove is type(plugin) or getattr(plugin, 'name', True) == remove:
                removed.append(plugin)
                del self.plugins[i]
                if hasattr(plugin, 'close'):
                    plugin.close()

        if removed:
            self.reset()
        return removed

    def reset(self, route=None):
        """ Reset all routes (force plugins to be re-applied) and clear all
            caches. If an ID or route object is given, only that specific route
            is affected. """
        global DEBUG
        if route is None:
            routes = self.routes
        elif isinstance(route, Route):
            routes = [route]
        else:
            routes = [
             self.routes[route]]
        for route in routes:
            route.reset()

        if DEBUG:
            for route in routes:
                route.prepare()

        return

    def close(self):
        """ Close the application and all installed plugins. """
        for plugin in self.plugins:
            if hasattr(plugin, 'close'):
                plugin.close()

        self.stopped = True

    def match(self, environ):
        """ Search for a matching route and return a (:class:`Route` , urlargs)
            tuple. The second value is a dictionary with parameters extracted
            from the URL. Raise :exc:`HTTPError` (404/405) on a non-match."""
        (route, args) = self.router.match(environ)
        return (route, args)

    def get_url(self, routename, **kargs):
        """ Return a string that matches a named route """
        scriptname = request.environ.get('SCRIPT_NAME', '').strip('/') + '/'
        location = self.router.build(routename, **kargs).lstrip('/')
        return urljoin(urljoin('/', scriptname), location)

    def route(self, path=None, method='GET', callback=None, name=None, apply=None, skip=None, **config):
        """ A decorator to bind a function to a request URL. Example::

                @app.route('/hello/:name')
                def hello(name):
                    return 'Hello %s' % name

            The ``:name`` part is a wildcard. See :class:`Router` for syntax
            details.

            :param path: Request path or a list of paths to listen to. If no
              path is specified, it is automatically generated from the
              signature of the function.
            :param method: HTTP method (`GET`, `POST`, `PUT`, ...) or a list of
              methods to listen to. (default: `GET`)
            :param callback: An optional shortcut to avoid the decorator
              syntax. ``route(..., callback=func)`` equals ``route(...)(func)``
            :param name: The name for this route. (default: None)
            :param apply: A decorator or plugin or a list of plugins. These are
              applied to the route callback in addition to installed plugins.
            :param skip: A list of plugins, plugin classes or names. Matching
              plugins are not installed to this route. ``True`` skips all.

            Any additional keyword arguments are stored as route-specific
            configuration and passed to plugins (see :meth:`Plugin.apply`).
        """
        if callable(path):
            path, callback = None, path
        plugins = makelist(apply)
        skiplist = makelist(skip)

        def decorator(callback):
            for rule in makelist(path) or yieldroutes(callback):
                for verb in makelist(method):
                    verb = verb.upper()
                    route = Route(self, rule, verb, callback, name=name, plugins=plugins, skiplist=skiplist, **config)
                    self.routes.append(route)
                    self.router.add(rule, verb, route, name=name)
                    if DEBUG:
                        route.prepare()

            return callback

        if callback:
            return decorator(callback)
        else:
            return decorator

    def get(self, path=None, method='GET', **options):
        """ Equals :meth:`route`. """
        return self.route(path, method, **options)

    def post(self, path=None, method='POST', **options):
        """ Equals :meth:`route` with a ``POST`` method parameter. """
        return self.route(path, method, **options)

    def put(self, path=None, method='PUT', **options):
        """ Equals :meth:`route` with a ``PUT`` method parameter. """
        return self.route(path, method, **options)

    def delete(self, path=None, method='DELETE', **options):
        """ Equals :meth:`route` with a ``DELETE`` method parameter. """
        return self.route(path, method, **options)

    def error(self, code=500):
        """ Decorator: Register an output handler for a HTTP error code"""

        def wrapper(handler):
            self.error_handler[int(code)] = handler
            return handler

        return wrapper

    def hook(self, name):
        """ Return a decorator that attaches a callback to a hook. """

        def wrapper(func):
            self.hooks.add(name, func)
            return func

        return wrapper

    def handle(self, path, method='GET'):
        """ (deprecated) Execute the first matching route callback and return
            the result. :exc:`HTTPResponse` exceptions are catched and returned.
            If :attr:`Bottle.catchall` is true, other exceptions are catched as
            well and returned as :exc:`HTTPError` instances (500).
        """
        depr('This method will change semantics in 0.10. Try to avoid it.')
        if isinstance(path, dict):
            return self._handle(path)
        return self._handle({'PATH_INFO': path, 'REQUEST_METHOD': method.upper()})

    def _handle(self, environ):
        try:
            (route, args) = self.match(environ)
            environ['route.handle'] = environ['bottle.route'] = route
            environ['route.url_args'] = args
            return route.call(**args)
        except HTTPResponse, r:
            return r
        except RouteReset:
            route.reset()
            return self._handle(environ)
        except (KeyboardInterrupt, SystemExit, MemoryError):
            raise
        except Exception, e:
            if not self.catchall:
                raise
            stacktrace = format_exc(10)
            environ['wsgi.errors'].write(stacktrace)
            return HTTPError(500, 'Internal Server Error', e, stacktrace)

    def _cast(self, out, request, response, peek=None):
        """ Try to convert the parameter into something WSGI compatible and set
        correct HTTP headers when possible.
        Support: False, str, unicode, dict, HTTPResponse, HTTPError, file-like,
        iterable of strings and iterable of unicodes
        """
        if not out:
            response['Content-Length'] = 0
            return []
        if isinstance(out, (tuple, list)) and isinstance(out[0], (bytes, unicode)):
            out = out[0][0:0].join(out)
        if isinstance(out, unicode):
            out = out.encode(response.charset)
        if isinstance(out, bytes):
            response['Content-Length'] = len(out)
            return [
             out]
        if isinstance(out, HTTPError):
            out.apply(response)
            out = self.error_handler.get(out.status, repr)(out)
            if isinstance(out, HTTPResponse):
                depr('Error handlers must not return :exc:`HTTPResponse`.')
            return self._cast(out, request, response)
        if isinstance(out, HTTPResponse):
            out.apply(response)
            return self._cast(out.output, request, response)
        if hasattr(out, 'read'):
            if 'wsgi.file_wrapper' in request.environ:
                return request.environ['wsgi.file_wrapper'](out)
            if hasattr(out, 'close') or not hasattr(out, '__iter__'):
                return WSGIFileWrapper(out)
        try:
            out = iter(out)
            first = out.next()
            while not first:
                first = out.next()

        except StopIteration:
            return self._cast('', request, response)
        except HTTPResponse, e:
            first = e
        except Exception, e:
            first = HTTPError(500, 'Unhandled exception', e, format_exc(10))
            if isinstance(e, (KeyboardInterrupt, SystemExit, MemoryError)) or not self.catchall:
                raise

        if isinstance(first, HTTPResponse):
            return self._cast(first, request, response)
        if isinstance(first, bytes):
            return itertools.chain([first], out)
        if isinstance(first, unicode):
            return itertools.imap(lambda x: x.encode(response.charset), itertools.chain([first], out))
        return self._cast(HTTPError(500, 'Unsupported response type: %s' % type(first)), request, response)

    def wsgi(self, environ, start_response):
        """ The bottle WSGI-interface. """
        try:
            environ['bottle.app'] = self
            request.bind(environ)
            response.bind()
            out = self._cast(self._handle(environ), request, response)
            if response.status_code in (100, 101, 204, 304) or request.method == 'HEAD':
                if hasattr(out, 'close'):
                    out.close()
                out = []
            start_response(response.status_line, list(response.iter_headers()))
            return out
        except (KeyboardInterrupt, SystemExit, MemoryError):
            raise
        except Exception, e:
            if not self.catchall:
                raise
            err = '<h1>Critical error while processing request: %s</h1>' % environ.get('PATH_INFO', '/')
            if DEBUG:
                err += '<h2>Error:</h2>\n<pre>%s</pre>\n' % repr(e)
                err += '<h2>Traceback:</h2>\n<pre>%s</pre>\n' % format_exc(10)
            environ['wsgi.errors'].write(err)
            start_response('500 INTERNAL SERVER ERROR', [('Content-Type', 'text/html')])
            return [tob(err)]

    def __call__(self, environ, start_response):
        return self.wsgi(environ, start_response)


class BaseRequest(DictMixin):
    """ A wrapper for WSGI environment dictionaries that adds a lot of
        convenient access methods and properties. Most of them are read-only."""
    MEMFILE_MAX = 102400

    def __init__(self, environ):
        """ Wrap a WSGI environ dictionary. """
        self.environ = environ
        environ['bottle.request'] = self

    @property
    def path(self):
        """ The value of ``PATH_INFO`` with exactly one prefixed slash (to fix
            broken clients and avoid the "empty path" edge case). """
        return '/' + self.environ.get('PATH_INFO', '').lstrip('/')

    @property
    def method(self):
        """ The ``REQUEST_METHOD`` value as an uppercase string. """
        return self.environ.get('REQUEST_METHOD', 'GET').upper()

    @DictProperty('environ', 'bottle.request.headers', read_only=True)
    def headers(self):
        """ A :class:`WSGIHeaderDict` that provides case-insensitive access to
            HTTP request headers. """
        return WSGIHeaderDict(self.environ)

    @DictProperty('environ', 'bottle.request.cookies', read_only=True)
    def cookies(self):
        """ Cookies parsed into a dictionary. Signed cookies are NOT decoded.
            Use :meth:`get_cookie` if you expect signed cookies. """
        raw_dict = SimpleCookie(self.environ.get('HTTP_COOKIE', ''))
        cookies = {}
        for cookie in raw_dict.itervalues():
            cookies[cookie.key] = cookie.value

        return cookies

    def get_cookie(self, key, default=None, secret=None):
        """ Return the content of a cookie. To read a `Signed Cookie`, the
            `secret` must match the one used to create the cookie (see
            :meth:`BaseResponse.set_cookie`). If anything goes wrong (missing
            cookie or wrong signature), return a default value. """
        value = self.cookies.get(key)
        if secret and value:
            dec = cookie_decode(value, secret)
            if dec and dec[0] == key:
                return dec[1]
            return default
        return value or default

    @DictProperty('environ', 'bottle.request.query', read_only=True)
    def query(self):
        """ The :attr:`query_string` parsed into a :class:`MultiDict`. These
            values are sometimes called "URL arguments" or "GET parameters", but
            not to be confused with "URL wildcards" as they are provided by the
            :class:`Router`. """
        data = parse_qs(self.query_string, keep_blank_values=True)
        get = self.environ['bottle.get'] = MultiDict()
        for (key, values) in data.iteritems():
            for value in values:
                get[key] = value

        return get

    @DictProperty('environ', 'bottle.request.forms', read_only=True)
    def forms(self):
        """ Form values parsed from an `url-encoded` or `multipart/form-data`
            encoded POST or PUT request body. The result is retuned as a
            :class:`MultiDict`. All keys and values are strings. File uploads
            are stored separately in :attr:`files`. """
        forms = MultiDict()
        for (name, item) in self.POST.iterallitems():
            if not hasattr(item, 'filename'):
                forms[name] = item

        return forms

    @DictProperty('environ', 'bottle.request.params', read_only=True)
    def params(self):
        """ A :class:`MultiDict` with the combined values of :attr:`query` and
            :attr:`forms`. File uploads are stored in :attr:`files`. """
        params = MultiDict()
        for (key, value) in self.query.iterallitems():
            params[key] = value

        for (key, value) in self.forms.iterallitems():
            params[key] = value

        return params

    @DictProperty('environ', 'bottle.request.files', read_only=True)
    def files(self):
        """ File uploads parsed from an `url-encoded` or `multipart/form-data`
            encoded POST or PUT request body. The values are instances of
            :class:`cgi.FieldStorage`. The most important attributes are:

            filename
                The filename, if specified; otherwise None; this is the client
                side filename, *not* the file name on which it is stored (that's
                a temporary file you don't deal with)
            file
                The file(-like) object from which you can read the data.
            value
                The value as a *string*; for file uploads, this transparently
                reads the file every time you request the value. Do not do this
                on big files.
        """
        files = MultiDict()
        for (name, item) in self.POST.iterallitems():
            if hasattr(item, 'filename'):
                files[name] = item

        return files

    @DictProperty('environ', 'bottle.request.json', read_only=True)
    def json(self):
        """ If the ``Content-Type`` header is ``application/json``, this
            property holds the parsed content of the request body. Only requests
            smaller than :attr:`MEMFILE_MAX` are processed to avoid memory
            exhaustion. """
        if self.environ.get('CONTENT_TYPE') == 'application/json' and 0 < self.content_length < self.MEMFILE_MAX:
            return json_loads(self.body.read(self.MEMFILE_MAX))
        else:
            return

    @DictProperty('environ', 'bottle.request.body', read_only=True)
    def _body(self):
        maxread = max(0, self.content_length)
        stream = self.environ['wsgi.input']
        body = BytesIO() if maxread < self.MEMFILE_MAX else TemporaryFile(mode='w+b')
        while maxread > 0:
            part = stream.read(min(maxread, self.MEMFILE_MAX))
            if not part:
                break
            body.write(part)
            maxread -= len(part)

        self.environ['wsgi.input'] = body
        body.seek(0)
        return body

    @property
    def body(self):
        """ The HTTP request body as a seek-able file-like object. Depending on
            :attr:`MEMFILE_MAX`, this is either a temporary file or a
            :class:`io.BytesIO` instance. Accessing this property for the first
            time reads and replaces the ``wsgi.input`` environ variable.
            Subsequent accesses just do a `seek(0)` on the file object. """
        self._body.seek(0)
        return self._body

    GET = query

    @DictProperty('environ', 'bottle.request.post', read_only=True)
    def POST(self):
        """ The values of :attr:`forms` and :attr:`files` combined into a single
            :class:`MultiDict`. Values are either strings (form values) or
            instances of :class:`cgi.FieldStorage` (file uploads).
        """
        post = MultiDict()
        safe_env = {'QUERY_STRING': ''}
        for key in ('REQUEST_METHOD', 'CONTENT_TYPE', 'CONTENT_LENGTH'):
            if key in self.environ:
                safe_env[key] = self.environ[key]

        if NCTextIOWrapper:
            fb = NCTextIOWrapper(self.body, encoding='ISO-8859-1', newline='\n')
        else:
            fb = self.body
        data = cgi.FieldStorage(fp=fb, environ=safe_env, keep_blank_values=True)
        for item in data.list or []:
            post[item.name] = item if item.filename else item.value

        return post

    @property
    def COOKIES(self):
        """ Alias for :attr:`cookies` (deprecated). """
        depr('BaseRequest.COOKIES was renamed to BaseRequest.cookies (lowercase).')
        return self.cookies

    @property
    def url(self):
        """ The full request URI including hostname and scheme. If your app
            lives behind a reverse proxy or load balancer and you get confusing
            results, make sure that the ``X-Forwarded-Host`` header is set
            correctly. """
        return self.urlparts.geturl()

    @DictProperty('environ', 'bottle.request.urlparts', read_only=True)
    def urlparts--- This code section failed: ---

 L. 991         0  LOAD_FAST             0  'self'
                3  LOAD_ATTR             0  'environ'
                6  STORE_FAST            1  'env'

 L. 992         9  LOAD_FAST             1  'env'
               12  LOAD_ATTR             1  'get'
               15  LOAD_CONST               'wsgi.url_scheme'
               18  LOAD_CONST               'http'
               21  CALL_FUNCTION_2       2  None
               24  STORE_FAST            2  'http'

 L. 993        27  LOAD_FAST             1  'env'
               30  LOAD_ATTR             1  'get'
               33  LOAD_CONST               'HTTP_X_FORWARDED_HOST'
               36  CALL_FUNCTION_1       1  None
               39  JUMP_IF_TRUE         13  'to 55'
               42  POP_TOP          
               43  LOAD_FAST             1  'env'
               46  LOAD_ATTR             1  'get'
               49  LOAD_CONST               'HTTP_HOST'
               52  CALL_FUNCTION_1       1  None
             55_0  COME_FROM            39  '39'
               55  STORE_FAST            3  'host'

 L. 994        58  LOAD_FAST             3  'host'
               61  JUMP_IF_TRUE         95  'to 159'
             64_0  THEN                     160
               64  POP_TOP          

 L. 996        65  LOAD_FAST             1  'env'
               68  LOAD_ATTR             1  'get'
               71  LOAD_CONST               'SERVER_NAME'
               74  LOAD_CONST               '127.0.0.1'
               77  CALL_FUNCTION_2       2  None
               80  STORE_FAST            3  'host'

 L. 997        83  LOAD_FAST             1  'env'
               86  LOAD_ATTR             1  'get'
               89  LOAD_CONST               'SERVER_PORT'
               92  CALL_FUNCTION_1       1  None
               95  STORE_FAST            4  'port'

 L. 998        98  LOAD_FAST             4  'port'
              101  JUMP_IF_FALSE        51  'to 155'
            104_0  THEN                     156
              104  POP_TOP          
              105  LOAD_FAST             4  'port'
              108  LOAD_FAST             2  'http'
              111  LOAD_CONST               'http'
              114  COMPARE_OP            2  ==
              117  JUMP_IF_FALSE         7  'to 127'
              120  POP_TOP          
              121  LOAD_CONST               '80'
              124  JUMP_FORWARD          4  'to 131'
            127_0  COME_FROM           117  '117'
              127  POP_TOP          
              128  LOAD_CONST               '443'
            131_0  COME_FROM           124  '124'
              131  COMPARE_OP            3  !=
              134  JUMP_IF_FALSE        18  'to 155'
              137  POP_TOP          

 L. 999       138  LOAD_FAST             3  'host'
              141  LOAD_CONST               ':'
              144  LOAD_FAST             4  'port'
              147  BINARY_ADD       
              148  INPLACE_ADD      
              149  STORE_FAST            3  'host'
              152  JUMP_ABSOLUTE       160  'to 160'
            155_0  COME_FROM           134  '134'
            155_1  COME_FROM           101  '101'
              155  POP_TOP          
              156  JUMP_FORWARD          1  'to 160'
            159_0  COME_FROM            61  '61'
              159  POP_TOP          
            160_0  COME_FROM           156  '156'

 L.1000       160  LOAD_GLOBAL           2  'urlquote'
              163  LOAD_FAST             0  'self'
              166  LOAD_ATTR             3  'fullpath'
              169  CALL_FUNCTION_1       1  None
              172  STORE_FAST            5  'path'

 L.1001       175  LOAD_GLOBAL           4  'UrlSplitResult'
              178  LOAD_FAST             2  'http'
              181  LOAD_FAST             3  'host'
              184  LOAD_FAST             5  'path'
              187  LOAD_FAST             1  'env'
              190  LOAD_ATTR             1  'get'
              193  LOAD_CONST               'QUERY_STRING'
              196  CALL_FUNCTION_1       1  None
              199  LOAD_CONST               ''
              202  CALL_FUNCTION_5       5  None
              205  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 205

    @property
    def fullpath(self):
        """ Request path including :attr:`script_name` (if present). """
        return urljoin(self.script_name, self.path.lstrip('/'))

    @property
    def query_string(self):
        """ The raw :attr:`query` part of the URL (everything in between ``?``
            and ``#``) as a string. """
        return self.environ.get('QUERY_STRING', '')

    @property
    def script_name(self):
        """ The initial portion of the URL's `path` that was removed by a higher
            level (server or routing middleware) before the application was
            called. This property returns an empty string, or a path with
            leading and tailing slashes. """
        script_name = self.environ.get('SCRIPT_NAME', '').strip('/')
        if script_name:
            return '/' + script_name + '/'
        return '/'

    def path_shift(self, shift=1):
        """ Shift path segments from :attr:`path` to :attr:`script_name` and
            vice versa.

           :param shift: The number of path segments to shift. May be negative
                         to change the shift direction. (default: 1)
        """
        script = self.environ.get('SCRIPT_NAME', '/')
        (self['SCRIPT_NAME'], self['PATH_INFO']) = path_shift(script, self.path, shift)

    @property
    def content_length(self):
        """ The request body length as an integer. The client is responsible to
            set this header. Otherwise, the real length of the body is unknown
            and -1 is returned. In this case, :attr:`body` will be empty. """
        return int(self.environ.get('CONTENT_LENGTH') or -1)

    @property
    def is_xhr(self):
        """ True if the request was triggered by a XMLHttpRequest. This only
            works with JavaScript libraries that support the `X-Requested-With`
            header (most of the popular libraries do). """
        requested_with = self.environ.get('HTTP_X_REQUESTED_WITH', '')
        return requested_with.lower() == 'xmlhttprequest'

    @property
    def is_ajax(self):
        """ Alias for :attr:`is_xhr`. "Ajax" is not the right term. """
        return self.is_xhr

    @property
    def auth(self):
        """ HTTP authentication data as a (user, password) tuple. This
            implementation currently supports basic (not digest) authentication
            only. If the authentication happened at a higher level (e.g. in the
            front web-server or a middleware), the password field is None, but
            the user field is looked up from the ``REMOTE_USER`` environ
            variable. On any errors, None is returned. """
        basic = parse_auth(self.environ.get('HTTP_AUTHORIZATION', ''))
        if basic:
            return basic
        else:
            ruser = self.environ.get('REMOTE_USER')
            if ruser:
                return (ruser, None)
            return

    @property
    def remote_route(self):
        """ A list of all IPs that were involved in this request, starting with
            the client IP and followed by zero or more proxies. This does only
            work if all proxies support the ```X-Forwarded-For`` header. Note
            that this information can be forged by malicious clients. """
        proxy = self.environ.get('HTTP_X_FORWARDED_FOR')
        if proxy:
            return [ ip.strip() for ip in proxy.split(',') ]
        remote = self.environ.get('REMOTE_ADDR')
        if remote:
            return [remote]
        return []

    @property
    def remote_addr(self):
        """ The client IP as a string. Note that this information can be forged
            by malicious clients. """
        route = self.remote_route
        if route:
            return route[0]
        else:
            return

    def copy(self):
        """ Return a new :class:`Request` with a shallow :attr:`environ` copy. """
        return Request(self.environ.copy())

    def __getitem__(self, key):
        return self.environ[key]

    def __delitem__(self, key):
        self[key] = ''
        del self.environ[key]

    def __iter__(self):
        return iter(self.environ)

    def __len__(self):
        return len(self.environ)

    def keys(self):
        return self.environ.keys()

    def __setitem__(self, key, value):
        """ Change an environ value and clear all caches that depend on it. """
        if self.environ.get('bottle.request.readonly'):
            raise KeyError('The environ dictionary is read-only.')
        self.environ[key] = value
        todelete = ()
        if key == 'wsgi.input':
            todelete = ('body', 'forms', 'files', 'params', 'post', 'json')
        elif key == 'QUERY_STRING':
            todelete = ('query', 'params')
        elif key.startswith('HTTP_'):
            todelete = ('headers', 'cookies')
        for key in todelete:
            self.environ.pop('bottle.request.' + key, None)

        return

    def __repr__(self):
        return '<%s: %s %s>' % (self.__class__.__name__, self.method, self.url)


def _hkey(s):
    return s.title().replace('_', '-')


class HeaderProperty(object):

    def __init__(self, name, reader=None, writer=str, default=''):
        (self.name, self.reader, self.writer, self.default) = (name, reader, writer, default)
        self.__doc__ = 'Current value of the %r header.' % name.title()

    def __get__(self, obj, cls):
        if obj is None:
            return self
        else:
            value = obj.headers.get(self.name)
            return value and (self.reader(value) if self.reader else value or self.default)

    def __set__(self, obj, value):
        if self.writer:
            value = self.writer(value)
        obj.headers[self.name] = value

    def __delete__(self, obj):
        if self.name in obj.headers:
            del obj.headers[self.name]


class BaseResponse(object):
    """ Storage class for a response body as well as headers and cookies.

        This class does support dict-like case-insensitive item-access to
        headers, but is NOT a dict. Most notably, iterating over a response
        yields parts of the body and not the headers.
    """
    default_status = 200
    default_content_type = 'text/html; charset=UTF-8'
    bad_headers = {204: set(('Content-Type', )), 
       304: set(('Allow', 'Content-Encoding', 'Content-Language', 'Content-Length', 'Content-Range',
     'Content-Type', 'Content-Md5', 'Last-Modified'))}

    def __init__(self, body='', status=None, **headers):
        self.status_code = None
        self.status_line = None
        self.body = body
        self._cookies = None
        self._headers = {'Content-Type': [self.default_content_type]}
        self.status = status or self.default_status
        if headers:
            for (name, value) in headers.items():
                self[name] = value

        return

    def copy(self):
        """ Returns a copy of self. """
        copy = Response()
        copy.status = self.status
        copy._headers = dict((k, v[:]) for (k, v) in self._headers.items())
        return copy

    def __iter__(self):
        return iter(self.body)

    def close(self):
        if hasattr(self.body, 'close'):
            self.body.close()

    def _set_status(self, status):
        if isinstance(status, int):
            code, status = status, _HTTP_STATUS_LINES.get(status)
        elif ' ' in status:
            status = status.strip()
            code = int(status.split()[0])
        else:
            raise ValueError('String status line without a reason phrase.')
        if not 100 <= code <= 999:
            raise ValueError('Status code out of range.')
        self.status_code = code
        self.status_line = status or '%d Unknown' % code

    status = property(lambda self: self.status_code, _set_status, None, ' A writeable property to change the HTTP response status. It accepts\n            either a numeric code (100-999) or a string with a custom reason\n            phrase (e.g. "404 Brain not found"). Both :data:`status_line` and\n            :data:`status_code` are updates accordingly. The return value is\n            always a numeric code. ')
    del _set_status

    @property
    def headers(self):
        """ An instance of :class:`HeaderDict`, a case-insensitive dict-like
            view on the response headers. """
        self.__dict__['headers'] = hdict = HeaderDict()
        hdict.dict = self._headers
        return hdict

    def __contains__(self, name):
        return _hkey(name) in self._headers

    def __delitem__(self, name):
        del self._headers[_hkey(name)]

    def __getitem__(self, name):
        return self._headers[_hkey(name)][(-1)]

    def __setitem__(self, name, value):
        self._headers[_hkey(name)] = [
         str(value)]

    def get_header(self, name, default=None):
        """ Return the value of a previously defined header. If there is no
            header with that name, return a default value. """
        return self._headers.get(_hkey(name), [default])[(-1)]

    def set_header(self, name, value, append=False):
        """ Create a new response header, replacing any previously defined
            headers with the same name. This equals ``response[name] = value``.

            :param append: Do not delete previously defined headers. This can
                           result in two (or more) headers having the same name.
        """
        if append:
            self._headers.setdefault(_hkey(name), []).append(str(value))
        else:
            self._headers[_hkey(name)] = [
             str(value)]

    def iter_headers(self):
        """ Yield (header, value) tuples, skipping headers that are not
            allowed with the current response status code. """
        headers = self._headers.iteritems()
        bad_headers = self.bad_headers.get(self.status_code)
        if bad_headers:
            headers = (h for h in headers if h[0] not in bad_headers)
        for (name, values) in headers:
            for value in values:
                yield (
                 name, value)

        if self._cookies:
            for c in self._cookies.values():
                yield (
                 'Set-Cookie', c.OutputString())

    def wsgiheader(self):
        depr('The wsgiheader method is deprecated. See headerlist.')
        return self.headerlist

    @property
    def headerlist(self):
        """ WSGI conform list of (header, value) tuples. """
        return list(self.iter_headers())

    content_type = HeaderProperty('Content-Type')
    content_length = HeaderProperty('Content-Length', reader=int)

    @property
    def charset(self):
        """ Return the charset specified in the content-type header (default: utf8). """
        if 'charset=' in self.content_type:
            return self.content_type.split('charset=')[(-1)].split(';')[0].strip()
        return 'UTF-8'

    @property
    def COOKIES(self):
        """ A dict-like SimpleCookie instance. This should not be used directly.
            See :meth:`set_cookie`. """
        depr('The COOKIES dict is deprecated. Use `set_cookie()` instead.')
        if not self._cookies:
            self._cookies = SimpleCookie()
        return self._cookies

    def set_cookie(self, key, value, secret=None, **options):
        """ Create a new cookie or replace an old one. If the `secret` parameter is
            set, create a `Signed Cookie` (described below).

            :param key: the name of the cookie.
            :param value: the value of the cookie.
            :param secret: a signature key required for signed cookies.

            Additionally, this method accepts all RFC 2109 attributes that are
            supported by :class:`cookie.Morsel`, including:

            :param max_age: maximum age in seconds. (default: None)
            :param expires: a datetime object or UNIX timestamp. (default: None)
            :param domain: the domain that is allowed to read the cookie.
              (default: current domain)
            :param path: limits the cookie to a given path (default: ``/``)
            :param secure: limit the cookie to HTTPS connections (default: off).
            :param httponly: prevents client-side javascript to read this cookie
              (default: off, requires Python 2.6 or newer).

            If neither `expires` nor `max_age` is set (default), the cookie will
            expire at the end of the browser session (as soon as the browser
            window is closed).

            Signed cookies may store any pickle-able object and are
            cryptographically signed to prevent manipulation. Keep in mind that
            cookies are limited to 4kb in most browsers.

            Warning: Signed cookies are not encrypted (the client can still see
            the content) and not copy-protected (the client can restore an old
            cookie). The main intention is to make pickling and unpickling
            save, not to store secret information at client side.
        """
        if not self._cookies:
            self._cookies = SimpleCookie()
        if secret:
            value = touni(cookie_encode((key, value), secret))
        elif not isinstance(value, basestring):
            raise TypeError('Secret key missing for non-string Cookie.')
        self._cookies[key] = value
        for (k, v) in options.iteritems():
            self._cookies[key][k.replace('_', '-')] = v

    def delete_cookie(self, key, **kwargs):
        """ Delete a cookie. Be sure to use the same `domain` and `path`
            settings as used to create the cookie. """
        kwargs['max_age'] = -1
        kwargs['expires'] = 0
        self.set_cookie(key, '', **kwargs)


class LocalRequest(BaseRequest, threading.local):
    """ A thread-local subclass of :class:`BaseRequest`. """

    def __init__(self):
        pass

    bind = BaseRequest.__init__


class LocalResponse(BaseResponse, threading.local):
    """ A thread-local subclass of :class:`BaseResponse`. """
    bind = BaseResponse.__init__


Response = LocalResponse
Request = LocalRequest

class JSONPlugin(object):
    name = 'json'

    def __init__(self, json_dumps=json_dumps):
        self.json_dumps = json_dumps

    def apply(self, callback, context):
        dumps = self.json_dumps
        if not dumps:
            return callback

        def wrapper(*a, **ka):
            rv = callback(*a, **ka)
            if isinstance(rv, dict):
                json_response = dumps(rv)
                response.content_type = 'application/json'
                return json_response
            return rv

        return wrapper


class HooksPlugin(object):
    name = 'hooks'

    def __init__(self):
        self.hooks = {'before_request': [], 'after_request': []}
        self.app = None
        return

    def _empty(self):
        return not (self.hooks['before_request'] or self.hooks['after_request'])

    def setup(self, app):
        self.app = app

    def add(self, name, func):
        """ Attach a callback to a hook. """
        if name not in self.hooks:
            raise ValueError('Unknown hook name %s' % name)
        was_empty = self._empty()
        self.hooks[name].append(func)
        if self.app and was_empty and not self._empty():
            self.app.reset()

    def remove(self, name, func):
        """ Remove a callback from a hook. """
        if name not in self.hooks:
            raise ValueError('Unknown hook name %s' % name)
        was_empty = self._empty()
        self.hooks[name].remove(func)
        if self.app and not was_empty and self._empty():
            self.app.reset()

    def apply(self, callback, context):
        if self._empty():
            return callback
        before_request = self.hooks['before_request']
        after_request = self.hooks['after_request']

        def wrapper(*a, **ka):
            for hook in before_request:
                hook()

            rv = callback(*a, **ka)
            for hook in after_request[::-1]:
                hook()

            return rv

        return wrapper


class TemplatePlugin(object):
    """ This plugin applies the :func:`view` decorator to all routes with a
        `template` config parameter. If the parameter is a tuple, the second
        element must be a dict with additional options (e.g. `template_engine`)
        or default variables for the template. """
    name = 'template'

    def apply(self, callback, context):
        conf = context['config'].get('template')
        if isinstance(conf, (tuple, list)) and len(conf) == 2:
            return view(conf[0], **conf[1])(callback)
        else:
            if isinstance(conf, str) and 'template_opts' in context['config']:
                depr('The `template_opts` parameter is deprecated.')
                return view(conf, **context['config']['template_opts'])(callback)
            if isinstance(conf, str):
                return view(conf)(callback)
            return callback


class _ImportRedirect(object):

    def __init__(self, name, impmask):
        """ Create a virtual package that redirects imports (see PEP 302). """
        self.name = name
        self.impmask = impmask
        self.module = sys.modules.setdefault(name, imp.new_module(name))
        self.module.__dict__.update({'__file__': __file__, '__path__': [], '__all__': [], '__loader__': self})
        sys.meta_path.append(self)

    def find_module(self, fullname, path=None):
        if '.' not in fullname:
            return
        (packname, modname) = fullname.rsplit('.', 1)
        if packname != self.name:
            return
        return self

    def load_module(self, fullname):
        if fullname in sys.modules:
            return sys.modules[fullname]
        (packname, modname) = fullname.rsplit('.', 1)
        realname = self.impmask % modname
        __import__(realname)
        module = sys.modules[fullname] = sys.modules[realname]
        setattr(self.module, modname, module)
        module.__loader__ = self
        return module


class MultiDict(DictMixin):
    """ This dict stores multiple values per key, but behaves exactly like a
        normal dict in that it returns only the newest value for any given key.
        There are special methods available to access the full list of values.
    """

    def __init__(self, *a, **k):
        self.dict = dict((k, [v]) for (k, v) in dict(*a, **k).iteritems())

    def __len__(self):
        return len(self.dict)

    def __iter__(self):
        return iter(self.dict)

    def __contains__(self, key):
        return key in self.dict

    def __delitem__(self, key):
        del self.dict[key]

    def __getitem__(self, key):
        return self.dict[key][(-1)]

    def __setitem__(self, key, value):
        self.append(key, value)

    def iterkeys(self):
        return self.dict.iterkeys()

    def itervalues(self):
        return (v[(-1)] for v in self.dict.itervalues())

    def iteritems(self):
        return ((k, v[(-1)]) for (k, v) in self.dict.iteritems())

    def iterallitems(self):
        for (key, values) in self.dict.iteritems():
            for value in values:
                yield (
                 key, value)

    keys = iterkeys if py3k else (lambda self: list(self.iterkeys()))
    values = itervalues if py3k else (lambda self: list(self.itervalues()))
    items = iteritems if py3k else (lambda self: list(self.iteritems()))
    allitems = iterallitems if py3k else (lambda self: list(self.iterallitems()))

    def get(self, key, default=None, index=-1):
        """ Return the current value for a key. The third `index` parameter
            defaults to -1 (last value). """
        if key in self.dict or default is KeyError:
            return self.dict[key][index]
        return default

    getone = get

    def append(self, key, value):
        """ Add a new value to the list of values for this key. """
        self.dict.setdefault(key, []).append(value)

    def replace(self, key, value):
        """ Replace the list of values with a single value. """
        self.dict[key] = [
         value]

    def getall(self, key):
        """ Return a (possibly empty) list of values for a key. """
        return self.dict.get(key) or []


class HeaderDict(MultiDict):
    """ A case-insensitive version of :class:`MultiDict` that defaults to
        replace the old value instead of appending it. """

    def __init__(self, *a, **ka):
        self.dict = {}
        if a or ka:
            self.update(*a, **ka)

    def __contains__(self, key):
        return _hkey(key) in self.dict

    def __delitem__(self, key):
        del self.dict[_hkey(key)]

    def __getitem__(self, key):
        return self.dict[_hkey(key)][(-1)]

    def __setitem__(self, key, value):
        self.dict[_hkey(key)] = [
         str(value)]

    def append(self, key, value):
        self.dict.setdefault(_hkey(key), []).append(str(value))

    def replace(self, key, value):
        self.dict[_hkey(key)] = [
         str(value)]

    def getall(self, key):
        return self.dict.get(_hkey(key)) or []

    def get(self, key, default=None, index=-1):
        return MultiDict.get(self, _hkey(key), default, index)

    def filter(self, names):
        for name in map(_hkey, names):
            if name in self.dict:
                del self.dict[name]


class WSGIHeaderDict(DictMixin):
    """ This dict-like class wraps a WSGI environ dict and provides convenient
        access to HTTP_* fields. Keys and values are native strings
        (2.x bytes or 3.x unicode) and keys are case-insensitive. If the WSGI
        environment contains non-native string values, these are de- or encoded
        using a lossless 'latin1' character set.

        The API will remain stable even on changes to the relevant PEPs.
        Currently PEP 333, 444 and 3333 are supported. (PEP 444 is the only one
        that uses non-native strings.)
    """
    cgikeys = ('CONTENT_TYPE', 'CONTENT_LENGTH')

    def __init__(self, environ):
        self.environ = environ

    def _ekey(self, key):
        """ Translate header field name to CGI/WSGI environ key. """
        key = key.replace('-', '_').upper()
        if key in self.cgikeys:
            return key
        return 'HTTP_' + key

    def raw(self, key, default=None):
        """ Return the header value as is (may be bytes or unicode). """
        return self.environ.get(self._ekey(key), default)

    def __getitem__(self, key):
        return tonat(self.environ[self._ekey(key)], 'latin1')

    def __setitem__(self, key, value):
        raise TypeError('%s is read-only.' % self.__class__)

    def __delitem__(self, key):
        raise TypeError('%s is read-only.' % self.__class__)

    def __iter__(self):
        for key in self.environ:
            if key[:5] == 'HTTP_':
                yield key[5:].replace('_', '-').title()
            elif key in self.cgikeys:
                yield key.replace('_', '-').title()

    def keys(self):
        return [ x for x in self ]

    def __len__(self):
        return len(self.keys())

    def __contains__(self, key):
        return self._ekey(key) in self.environ


class AppStack(list):
    """ A stack-like list. Calling it returns the head of the stack. """

    def __call__(self):
        """ Return the current default application. """
        return self[(-1)]

    def push(self, value=None):
        """ Add a new :class:`Bottle` instance to the stack """
        if not isinstance(value, Bottle):
            value = Bottle()
        self.append(value)
        return value


class WSGIFileWrapper(object):

    def __init__(self, fp, buffer_size=65536):
        self.fp, self.buffer_size = fp, buffer_size
        for attr in ('fileno', 'close', 'read', 'readlines'):
            if hasattr(fp, attr):
                setattr(self, attr, getattr(fp, attr))

    def __iter__(self):
        read, buff = self.fp.read, self.buffer_size
        while True:
            part = read(buff)
            if not part:
                break
            yield part


def abort(code=500, text='Unknown Error: Application stopped.'):
    """ Aborts execution and causes a HTTP error. """
    raise HTTPError(code, text)


def redirect(url, code=None):
    """ Aborts execution and causes a 303 or 302 redirect, depending on
        the HTTP protocol version. """
    if code is None:
        code = 303 if request.get('SERVER_PROTOCOL') == 'HTTP/1.1' else 302
    location = urljoin(request.url, url)
    raise HTTPResponse('', status=code, header=dict(Location=location))
    return


def static_file(filename, root, mimetype='auto', download=False):
    """ Open a file in a safe way and return :exc:`HTTPResponse` with status
        code 200, 305, 401 or 404. Set Content-Type, Content-Encoding,
        Content-Length and Last-Modified header. Obey If-Modified-Since header
        and HEAD requests.
    """
    root = os.path.abspath(root) + os.sep
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    header = dict()
    if not filename.startswith(root):
        return HTTPError(403, 'Access denied.')
    else:
        if not os.path.exists(filename) or not os.path.isfile(filename):
            return HTTPError(404, 'File does not exist.')
        if not os.access(filename, os.R_OK):
            return HTTPError(403, 'You do not have permission to access this file.')
        if mimetype == 'auto':
            (mimetype, encoding) = mimetypes.guess_type(filename)
            if mimetype:
                header['Content-Type'] = mimetype
            if encoding:
                header['Content-Encoding'] = encoding
        elif mimetype:
            header['Content-Type'] = mimetype
        if download:
            download = os.path.basename(filename if download == True else download)
            header['Content-Disposition'] = 'attachment; filename="%s"' % download
        stats = os.stat(filename)
        header['Content-Length'] = stats.st_size
        lm = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime(stats.st_mtime))
        header['Last-Modified'] = lm
        ims = request.environ.get('HTTP_IF_MODIFIED_SINCE')
        if ims:
            ims = parse_date(ims.split(';')[0].strip())
        if ims is not None and ims >= int(stats.st_mtime):
            header['Date'] = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime())
            return HTTPResponse(status=304, header=header)
        body = '' if request.method == 'HEAD' else open(filename, 'rb')
        return HTTPResponse(body, header=header)


def debug(mode=True):
    """ Change the debug level.
    There is only one debug level supported at the moment."""
    global DEBUG
    DEBUG = bool(mode)


def parse_date(ims):
    """ Parse rfc1123, rfc850 and asctime timestamps and return UTC epoch. """
    try:
        ts = email.utils.parsedate_tz(ims)
        return time.mktime(ts[:8] + (0, )) - (ts[9] or 0) - time.timezone
    except (TypeError, ValueError, IndexError, OverflowError):
        return

    return


def parse_auth(header):
    """ Parse rfc2617 HTTP authentication header string (basic) and return (user,pass) tuple or None"""
    try:
        (method, data) = header.split(None, 1)
        if method.lower() == 'basic':
            (user, pwd) = touni(base64.b64decode(tob(data))).split(':', 1)
            return (
             user, pwd)
    except (KeyError, ValueError):
        return

    return


def _lscmp(a, b):
    """ Compares two strings in a cryptographically save way:
        Runtime is not affected by length of common prefix. """
    return not sum((0 if x == y else 1) for (x, y) in zip(a, b)) and len(a) == len(b)


def cookie_encode(data, key):
    """ Encode and sign a pickle-able object. Return a (byte) string """
    msg = base64.b64encode(pickle.dumps(data, -1))
    sig = base64.b64encode(hmac.new(key, msg).digest())
    return tob('!') + sig + tob('?') + msg


def cookie_decode(data, key):
    """ Verify and decode an encoded string. Return an object or None."""
    data = tob(data)
    if cookie_is_encoded(data):
        (sig, msg) = data.split(tob('?'), 1)
        if _lscmp(sig[1:], base64.b64encode(hmac.new(key, msg).digest())):
            return pickle.loads(base64.b64decode(msg))
    return


def cookie_is_encoded(data):
    """ Return True if the argument looks like a encoded cookie."""
    return bool(data.startswith(tob('!')) and tob('?') in data)


def html_escape(string):
    """ Escape HTML special characters ``&<>`` and quotes ``'"``. """
    return string.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#039;')


def html_quote(string):
    """ Escape and quote a string to be used as an HTTP attribute."""
    return '"%s"' % html_escape(string).replace('\n', '%#10;').replace('\r', '&#13;').replace('\t', '&#9;')


def yieldroutes(func):
    """ Return a generator for routes that match the signature (name, args)
    of the func parameter. This may yield more than one route if the function
    takes optional keyword arguments. The output is best described by example::

        a()         -> '/a'
        b(x, y)     -> '/b/:x/:y'
        c(x, y=5)   -> '/c/:x' and '/c/:x/:y'
        d(x=5, y=6) -> '/d' and '/d/:x' and '/d/:x/:y'
    """
    import inspect
    path = '/' + func.__name__.replace('__', '/').lstrip('/')
    spec = inspect.getargspec(func)
    argc = len(spec[0]) - len(spec[3] or [])
    path += '/:%s' * argc % tuple(spec[0][:argc])
    yield path
    for arg in spec[0][argc:]:
        path += '/:%s' % arg
        yield path


def path_shift(script_name, path_info, shift=1):
    """ Shift path fragments from PATH_INFO to SCRIPT_NAME and vice versa.

        :return: The modified paths.
        :param script_name: The SCRIPT_NAME path.
        :param script_name: The PATH_INFO path.
        :param shift: The number of path fragments to shift. May be negative to
          change the shift direction. (default: 1)
    """
    if shift == 0:
        return (script_name, path_info)
    pathlist = path_info.strip('/').split('/')
    scriptlist = script_name.strip('/').split('/')
    if pathlist and pathlist[0] == '':
        pathlist = []
    if scriptlist and scriptlist[0] == '':
        scriptlist = []
    if shift > 0 and shift <= len(pathlist):
        moved = pathlist[:shift]
        scriptlist = scriptlist + moved
        pathlist = pathlist[shift:]
    elif shift < 0 and shift >= -len(scriptlist):
        moved = scriptlist[shift:]
        pathlist = moved + pathlist
        scriptlist = scriptlist[:shift]
    else:
        empty = 'SCRIPT_NAME' if shift < 0 else 'PATH_INFO'
        raise AssertionError('Cannot shift. Nothing left from %s' % empty)
    new_script_name = '/' + ('/').join(scriptlist)
    new_path_info = '/' + ('/').join(pathlist)
    if path_info.endswith('/') and pathlist:
        new_path_info += '/'
    return (
     new_script_name, new_path_info)


def validate(**vkargs):
    """
    Validates and manipulates keyword arguments by user defined callables.
    Handles ValueError and missing arguments by raising HTTPError(403).
    """

    def decorator(func):

        def wrapper(**kargs):
            for (key, value) in vkargs.iteritems():
                if key not in kargs:
                    abort(403, 'Missing parameter: %s' % key)
                try:
                    kargs[key] = value(kargs[key])
                except ValueError:
                    abort(403, 'Wrong parameter format for: %s' % key)

            return func(**kargs)

        return wrapper

    return decorator


def auth_basic(check, realm='private', text='Access denied'):
    """ Callback decorator to require HTTP auth (basic).
        TODO: Add route(check_auth=...) parameter. """

    def decorator(func):

        def wrapper(*a, **ka):
            (user, password) = request.auth or (None, None)
            if user is None or not check(user, password):
                response.headers['WWW-Authenticate'] = 'Basic realm="%s"' % realm
                return HTTPError(401, text)
            else:
                return func(*a, **ka)

        return wrapper

    return decorator


def make_default_app_wrapper(name):
    """ Return a callable that relays calls to the current default app. """

    @functools.wraps(getattr(Bottle, name))
    def wrapper(*a, **ka):
        return getattr(app(), name)(*a, **ka)

    return wrapper


for name in ('route get post put delete error mount\n               hook install uninstall').split():
    globals()[name] = make_default_app_wrapper(name)

url = make_default_app_wrapper('get_url')
del name

class ServerAdapter(object):
    quiet = False

    def __init__(self, host='127.0.0.1', port=8080, **config):
        self.options = config
        self.host = host
        self.port = int(port)

    def run(self, handler):
        pass

    def __repr__(self):
        args = (', ').join([ '%s=%s' % (k, repr(v)) for (k, v) in self.options.items() ])
        return '%s(%s)' % (self.__class__.__name__, args)


class CGIServer(ServerAdapter):
    quiet = True

    def run(self, handler):
        from wsgiref.handlers import CGIHandler

        def fixed_environ(environ, start_response):
            environ.setdefault('PATH_INFO', '')
            return handler(environ, start_response)

        CGIHandler().run(fixed_environ)


class FlupFCGIServer(ServerAdapter):

    def run(self, handler):
        import flup.server.fcgi
        self.options.setdefault('bindAddress', (self.host, self.port))
        flup.server.fcgi.WSGIServer(handler, **self.options).run()


class WSGIRefServer(ServerAdapter):

    def run(self, handler):
        from wsgiref.simple_server import make_server, WSGIRequestHandler
        if self.quiet:

            class QuietHandler(WSGIRequestHandler):

                def log_request(*args, **kw):
                    pass

            self.options['handler_class'] = QuietHandler
        srv = make_server(self.host, self.port, handler, **self.options)
        srv.serve_forever()


class CherryPyServer(ServerAdapter):

    def run(self, handler):
        from cherrypy import wsgiserver
        server = wsgiserver.CherryPyWSGIServer((self.host, self.port), handler)
        try:
            server.start()
        finally:
            server.stop()


class PasteServer(ServerAdapter):

    def run(self, handler):
        from paste import httpserver
        if not self.quiet:
            from paste.translogger import TransLogger
            handler = TransLogger(handler)
        httpserver.serve(handler, host=self.host, port=str(self.port), **self.options)


class MeinheldServer(ServerAdapter):

    def run(self, handler):
        from meinheld import server
        server.listen((self.host, self.port))
        server.run(handler)


class FapwsServer(ServerAdapter):
    """ Extremely fast webserver using libev. See http://www.fapws.org/ """

    def run(self, handler):
        import fapws._evwsgi as evwsgi
        from fapws import base, config
        port = self.port
        if float(config.SERVER_IDENT[-2:]) > 0.4:
            port = str(port)
        evwsgi.start(self.host, port)
        if 'BOTTLE_CHILD' in os.environ and not self.quiet:
            print 'WARNING: Auto-reloading does not work with Fapws3.'
            print '         (Fapws3 breaks python thread support)'
        evwsgi.set_base_module(base)

        def app(environ, start_response):
            environ['wsgi.multiprocess'] = False
            return handler(environ, start_response)

        evwsgi.wsgi_cb(('', app))
        evwsgi.run()


class TornadoServer(ServerAdapter):
    """ The super hyped asynchronous server by facebook. Untested. """

    def run(self, handler):
        import tornado.wsgi, tornado.httpserver, tornado.ioloop
        container = tornado.wsgi.WSGIContainer(handler)
        server = tornado.httpserver.HTTPServer(container)
        server.listen(port=self.port)
        tornado.ioloop.IOLoop.instance().start()


class AppEngineServer(ServerAdapter):
    """ Adapter for Google App Engine. """
    quiet = True

    def run(self, handler):
        from google.appengine.ext.webapp import util
        module = sys.modules.get('__main__')
        if module and not hasattr(module, 'main'):
            module.main = lambda : util.run_wsgi_app(handler)
        util.run_wsgi_app(handler)


class TwistedServer(ServerAdapter):
    """ Untested. """

    def run(self, handler):
        from twisted.web import server, wsgi
        from twisted.python.threadpool import ThreadPool
        from twisted.internet import reactor
        thread_pool = ThreadPool()
        thread_pool.start()
        reactor.addSystemEventTrigger('after', 'shutdown', thread_pool.stop)
        factory = server.Site(wsgi.WSGIResource(reactor, thread_pool, handler))
        reactor.listenTCP(self.port, factory, interface=self.host)
        reactor.run()


class DieselServer(ServerAdapter):
    """ Untested. """

    def run(self, handler):
        from diesel.protocols.wsgi import WSGIApplication
        app = WSGIApplication(handler, port=self.port)
        app.run()


class GeventServer(ServerAdapter):
    """ Untested. Options:

        * `monkey` (default: True) fixes the stdlib to use greenthreads.
        * `fast` (default: False) uses libevent's http server, but has some
          issues: No streaming, no pipelining, no SSL.
    """

    def run(self, handler):
        from gevent import wsgi as wsgi_fast, pywsgi, monkey, local
        if self.options.get('monkey', True):
            if threading.local is not local.local:
                monkey.patch_all()
        wsgi = wsgi_fast if self.options.get('fast') else pywsgi
        wsgi.WSGIServer((self.host, self.port), handler).serve_forever()


class GunicornServer(ServerAdapter):
    """ Untested. """

    def run(self, handler):
        from gunicorn.arbiter import Arbiter
        from gunicorn.config import Config
        handler.cfg = Config({'bind': '%s:%d' % (self.host, self.port), 'workers': 4})
        arbiter = Arbiter(handler)
        arbiter.run()


class EventletServer(ServerAdapter):
    """ Untested """

    def run(self, handler):
        from eventlet import wsgi, listen
        wsgi.server(listen((self.host, self.port)), handler)


class RocketServer(ServerAdapter):
    """ Untested. """

    def run(self, handler):
        from rocket import Rocket
        server = Rocket((self.host, self.port), 'wsgi', {'wsgi_app': handler})
        server.start()


class BjoernServer(ServerAdapter):
    """ Fast server written in C: https://github.com/jonashaag/bjoern """

    def run(self, handler):
        from bjoern import run
        run(handler, self.host, self.port)


class AutoServer(ServerAdapter):
    """ Untested. """
    adapters = [
     PasteServer, CherryPyServer, TwistedServer, WSGIRefServer]

    def run(self, handler):
        for sa in self.adapters:
            try:
                return sa(self.host, self.port, **self.options).run(handler)
            except ImportError:
                pass


server_names = {'cgi': CGIServer, 
   'flup': FlupFCGIServer, 
   'wsgiref': WSGIRefServer, 
   'cherrypy': CherryPyServer, 
   'paste': PasteServer, 
   'fapws3': FapwsServer, 
   'tornado': TornadoServer, 
   'gae': AppEngineServer, 
   'twisted': TwistedServer, 
   'diesel': DieselServer, 
   'meinheld': MeinheldServer, 
   'gunicorn': GunicornServer, 
   'eventlet': EventletServer, 
   'gevent': GeventServer, 
   'rocket': RocketServer, 
   'bjoern': BjoernServer, 
   'auto': AutoServer}

def load(target, **namespace):
    """ Import a module or fetch an object from a module.

        * ``package.module`` returns `module` as a module object.
        * ``pack.mod:name`` returns the module variable `name` from `pack.mod`.
        * ``pack.mod:func()`` calls `pack.mod.func()` and returns the result.

        The last form accepts not only function calls, but any type of
        expression. Keyword arguments passed to this function are available as
        local variables. Example: ``import_string('re:compile(x)', x='[a-z]')``
    """
    (module, target) = target.split(':', 1) if ':' in target else (target, None)
    if module not in sys.modules:
        __import__(module)
    if not target:
        return sys.modules[module]
    else:
        if target.isalnum():
            return getattr(sys.modules[module], target)
        package_name = module.split('.')[0]
        namespace[package_name] = sys.modules[package_name]
        return eval('%s.%s' % (module, target), namespace)


def load_app(target):
    """ Load a bottle application from a module and make sure that the import
        does not affect the current default application, but returns a separate
        application object. See :func:`load` for details. """
    tmp = app.push()
    rv = _load(target)
    app.remove(tmp)
    if isinstance(rv, Bottle):
        return rv
    return tmp


def run(app=None, server='wsgiref', host='127.0.0.1', port=8080, interval=1, reloader=False, quiet=False, **kargs):
    """ Start a server instance. This method blocks until the server terminates.

        :param app: WSGI application or target string supported by
               :func:`load_app`. (default: :func:`default_app`)
        :param server: Server adapter to use. See :data:`server_names` keys
               for valid names or pass a :class:`ServerAdapter` subclass.
               (default: `wsgiref`)
        :param host: Server address to bind to. Pass ``0.0.0.0`` to listens on
               all interfaces including the external one. (default: 127.0.0.1)
        :param port: Server port to bind to. Values below 1024 require root
               privileges. (default: 8080)
        :param reloader: Start auto-reloading server? (default: False)
        :param interval: Auto-reloader interval in seconds (default: 1)
        :param quiet: Suppress output to stdout and stderr? (default: False)
        :param options: Options passed to the server adapter.
     """
    app = app or default_app()
    if isinstance(app, basestring):
        app = load_app(app)
    if isinstance(server, basestring):
        server = server_names.get(server)
    if isinstance(server, type):
        server = server(host=host, port=port, **kargs)
    if not isinstance(server, ServerAdapter):
        raise RuntimeError('Server must be a subclass of ServerAdapter')
    server.quiet = server.quiet or quiet
    if not server.quiet and not os.environ.get('BOTTLE_CHILD'):
        print 'Bottle server starting up (using %s)...' % repr(server)
        print 'Listening on http://%s:%d/' % (server.host, server.port)
        print 'Use Ctrl-C to quit.'
        print
    try:
        if reloader:
            interval = min(interval, 1)
            if os.environ.get('BOTTLE_CHILD'):
                _reloader_child(server, app, interval)
            else:
                _reloader_observer(server, app, interval)
        else:
            server.run(app)
    except KeyboardInterrupt:
        pass

    if not server.quiet and not os.environ.get('BOTTLE_CHILD'):
        print 'Shutting down...'


class FileCheckerThread(threading.Thread):
    """ Thread that periodically checks for changed module files. """

    def __init__(self, lockfile, interval):
        threading.Thread.__init__(self)
        self.lockfile, self.interval = lockfile, interval
        self.status = 0

    def run(self):
        exists = os.path.exists
        mtime = lambda path: os.stat(path).st_mtime
        files = dict()
        for module in sys.modules.values():
            path = getattr(module, '__file__', '')
            if path[-4:] in ('.pyo', '.pyc'):
                path = path[:-1]
            if path and exists(path):
                files[path] = mtime(path)

        while not self.status:
            for (path, lmtime) in files.iteritems():
                if not exists(path) or mtime(path) > lmtime:
                    self.status = 3

            if not exists(self.lockfile):
                self.status = 2
            elif mtime(self.lockfile) < time.time() - self.interval - 5:
                self.status = 1
            if not self.status:
                time.sleep(self.interval)

        if self.status != 5:
            thread.interrupt_main()


def _reloader_child(server, app, interval):
    """ Start the server and check for modified files in a background thread.
        As soon as an update is detected, KeyboardInterrupt is thrown in
        the main thread to exit the server loop. The process exists with status
        code 3 to request a reload by the observer process. If the lockfile
        is not modified in 2*interval second or missing, we assume that the
        observer process died and exit with status code 1 or 2.
    """
    lockfile = os.environ.get('BOTTLE_LOCKFILE')
    bgcheck = FileCheckerThread(lockfile, interval)
    try:
        bgcheck.start()
        server.run(app)
    except KeyboardInterrupt:
        pass

    bgcheck.status, status = 5, bgcheck.status
    bgcheck.join()
    if status:
        sys.exit(status)


def _reloader_observer(server, app, interval):
    """ Start a child process with identical commandline arguments and restart
        it as long as it exists with status code 3. Also create a lockfile and
        touch it (update mtime) every interval seconds.
    """
    (fd, lockfile) = tempfile.mkstemp(prefix='bottle-reloader.', suffix='.lock')
    os.close(fd)
    try:
        while os.path.exists(lockfile):
            args = [
             sys.executable] + sys.argv
            environ = os.environ.copy()
            environ['BOTTLE_CHILD'] = 'true'
            environ['BOTTLE_LOCKFILE'] = lockfile
            p = subprocess.Popen(args, env=environ)
            while p.poll() is None:
                os.utime(lockfile, None)
                time.sleep(interval)

            if p.poll() != 3:
                if os.path.exists(lockfile):
                    os.unlink(lockfile)
                sys.exit(p.poll())
            elif not server.quiet:
                print 'Reloading server...'

    except KeyboardInterrupt:
        pass

    if os.path.exists(lockfile):
        os.unlink(lockfile)
    return


class TemplateError(HTTPError):

    def __init__(self, message):
        HTTPError.__init__(self, 500, message)


class BaseTemplate(object):
    """ Base class and minimal API for template adapters """
    extentions = [
     'tpl', 'html', 'thtml', 'stpl']
    settings = {}
    defaults = {}

    def __init__(self, source=None, name=None, lookup=[], encoding='utf8', **settings):
        """ Create a new template.
        If the source parameter (str or buffer) is missing, the name argument
        is used to guess a template filename. Subclasses can assume that
        self.source and/or self.filename are set. Both are strings.
        The lookup, encoding and settings parameters are stored as instance
        variables.
        The lookup parameter stores a list containing directory paths.
        The encoding parameter should be used to decode byte strings or files.
        The settings parameter contains a dict for engine-specific settings.
        """
        self.name = name
        self.source = source.read() if hasattr(source, 'read') else source
        self.filename = source.filename if hasattr(source, 'filename') else None
        self.lookup = map(os.path.abspath, lookup)
        self.encoding = encoding
        self.settings = self.settings.copy()
        self.settings.update(settings)
        if not self.source and self.name:
            self.filename = self.search(self.name, self.lookup)
            if not self.filename:
                raise TemplateError('Template %s not found.' % repr(name))
        if not self.source and not self.filename:
            raise TemplateError('No template specified.')
        self.prepare(**self.settings)
        return

    @classmethod
    def search(cls, name, lookup=[]):
        """ Search name in all directories specified in lookup.
        First without, then with common extensions. Return first hit. """
        if os.path.isfile(name):
            return name
        for spath in lookup:
            fname = os.path.join(spath, name)
            if os.path.isfile(fname):
                return fname
            for ext in cls.extentions:
                if os.path.isfile('%s.%s' % (fname, ext)):
                    return '%s.%s' % (fname, ext)

    @classmethod
    def global_config(cls, key, *args):
        """ This reads or sets the global settings stored in class.settings. """
        if args:
            cls.settings[key] = args[0]
        else:
            return cls.settings[key]

    def prepare(self, **options):
        """ Run preparations (parsing, caching, ...).
        It should be possible to call this again to refresh a template or to
        update settings.
        """
        raise NotImplementedError

    def render(self, *args, **kwargs):
        """ Render the template with the specified local variables and return
        a single byte or unicode string. If it is a byte string, the encoding
        must match self.encoding. This method must be thread-safe!
        Local variables may be provided in dictionaries (*args)
        or directly, as keywords (**kwargs).
        """
        raise NotImplementedError


class MakoTemplate(BaseTemplate):

    def prepare(self, **options):
        from mako.template import Template
        from mako.lookup import TemplateLookup
        options.update({'input_encoding': self.encoding})
        options.setdefault('format_exceptions', bool(DEBUG))
        lookup = TemplateLookup(directories=self.lookup, **options)
        if self.source:
            self.tpl = Template(self.source, lookup=lookup, **options)
        else:
            self.tpl = Template(uri=self.name, filename=self.filename, lookup=lookup, **options)

    def render(self, *args, **kwargs):
        for dictarg in args:
            kwargs.update(dictarg)

        _defaults = self.defaults.copy()
        _defaults.update(kwargs)
        return self.tpl.render(**_defaults)


class CheetahTemplate(BaseTemplate):

    def prepare(self, **options):
        from Cheetah.Template import Template
        self.context = threading.local()
        self.context.vars = {}
        options['searchList'] = [self.context.vars]
        if self.source:
            self.tpl = Template(source=self.source, **options)
        else:
            self.tpl = Template(file=self.filename, **options)

    def render(self, *args, **kwargs):
        for dictarg in args:
            kwargs.update(dictarg)

        self.context.vars.update(self.defaults)
        self.context.vars.update(kwargs)
        out = str(self.tpl)
        self.context.vars.clear()
        return out


class Jinja2Template(BaseTemplate):

    def prepare(self, filters=None, tests=None, **kwargs):
        from jinja2 import Environment, FunctionLoader
        if 'prefix' in kwargs:
            raise RuntimeError('The keyword argument `prefix` has been removed. Use the full jinja2 environment name line_statement_prefix instead.')
        self.env = Environment(loader=FunctionLoader(self.loader), **kwargs)
        if filters:
            self.env.filters.update(filters)
        if tests:
            self.env.tests.update(tests)
        if self.source:
            self.tpl = self.env.from_string(self.source)
        else:
            self.tpl = self.env.get_template(self.filename)

    def render(self, *args, **kwargs):
        for dictarg in args:
            kwargs.update(dictarg)

        _defaults = self.defaults.copy()
        _defaults.update(kwargs)
        return self.tpl.render(**_defaults)

    def loader(self, name):
        fname = self.search(name, self.lookup)
        if fname:
            with open(fname, 'rb') as (f):
                return f.read().decode(self.encoding)


class SimpleTALTemplate(BaseTemplate):
    """ Untested! """

    def prepare(self, **options):
        from simpletal import simpleTAL
        if self.source:
            self.tpl = simpleTAL.compileHTMLTemplate(self.source)
        else:
            with open(self.filename, 'rb') as (fp):
                self.tpl = simpleTAL.compileHTMLTemplate(tonat(fp.read()))

    def render(self, *args, **kwargs):
        from simpletal import simpleTALES
        from StringIO import StringIO
        for dictarg in args:
            kwargs.update(dictarg)

        context = simpleTALES.Context()
        for (k, v) in self.defaults.items():
            context.addGlobal(k, v)

        for (k, v) in kwargs.items():
            context.addGlobal(k, v)

        output = StringIO()
        self.tpl.expand(context, output)
        return output.getvalue()


class SimpleTemplate(BaseTemplate):
    blocks = ('if', 'elif', 'else', 'try', 'except', 'finally', 'for', 'while', 'with',
              'def', 'class')
    dedent_blocks = ('elif', 'else', 'except', 'finally')

    @lazy_attribute
    def re_pytokens(cls):
        """ This matches comments and all kinds of quoted strings but does
            NOT match comments (#...) within quoted strings. (trust me) """
        return re.compile('\n            (\'\'(?!\')|""(?!")|\'{6}|"{6}    # Empty strings (all 4 types)\n             |\'(?:[^\\\\\']|\\\\.)+?\'          # Single quotes (\')\n             |"(?:[^\\\\"]|\\\\.)+?"          # Double quotes (")\n             |\'{3}(?:[^\\\\]|\\\\.|\\n)+?\'{3}  # Triple-quoted strings (\')\n             |"{3}(?:[^\\\\]|\\\\.|\\n)+?"{3}  # Triple-quoted strings (")\n             |\\#.*                        # Comments\n            )', re.VERBOSE)

    def prepare(self, escape_func=html_escape, noescape=False):
        self.cache = {}
        enc = self.encoding
        self._str = lambda x: touni(x, enc)
        self._escape = lambda x: escape_func(touni(x, enc))
        if noescape:
            self._str, self._escape = self._escape, self._str

    @classmethod
    def split_comment(cls, code):
        """ Removes comments (#...) from python code. """
        if '#' not in code:
            return code
        subf = lambda m: '' if m.group(0)[0] == '#' else m.group(0)
        return re.sub(cls.re_pytokens, subf, code)

    @cached_property
    def co(self):
        return compile(self.code, self.filename or '<string>', 'exec')

    @cached_property
    def code(self):
        stack = []
        lineno = 0
        ptrbuffer = []
        codebuffer = []
        multiline = dedent = oneline = False
        template = self.source if self.source else open(self.filename).read()

        def yield_tokens(line):
            for (i, part) in enumerate(re.split('\\{\\{(.*?)\\}\\}', line)):
                if i % 2:
                    if part.startswith('!'):
                        yield ('RAW', part[1:])
                    else:
                        yield (
                         'CMD', part)
                else:
                    yield (
                     'TXT', part)

        def flush():
            if not ptrbuffer:
                return
            cline = ''
            for line in ptrbuffer:
                for (token, value) in line:
                    if token == 'TXT':
                        cline += repr(value)
                    elif token == 'RAW':
                        cline += '_str(%s)' % value
                    elif token == 'CMD':
                        cline += '_escape(%s)' % value
                    cline += ', '

                cline = cline[:-2] + '\\\n'

            cline = cline[:-2]
            if cline[:-1].endswith('\\\\\\\\\\n'):
                cline = cline[:-7] + cline[(-1)]
            cline = '_printlist([' + cline + '])'
            del ptrbuffer[:]
            code(cline)

        def code(stmt):
            for line in stmt.splitlines():
                codebuffer.append('  ' * len(stack) + line.strip())

        for line in template.splitlines(True):
            lineno += 1
            line = line if isinstance(line, unicode) else unicode(line, encoding=self.encoding)
            if lineno <= 2:
                m = re.search('%.*coding[:=]\\s*([-\\w\\.]+)', line)
                if m:
                    self.encoding = m.group(1)
                if m:
                    line = line.replace('coding', 'coding (removed)')
            if line.strip()[:2].count('%') == 1:
                line = line.split('%', 1)[1].lstrip()
                cline = self.split_comment(line).strip()
                cmd = re.split('[^a-zA-Z0-9_]', cline)[0]
                flush()
                if cmd in self.blocks or multiline:
                    cmd = multiline or cmd
                    dedent = cmd in self.dedent_blocks
                    if dedent and not oneline and not multiline:
                        cmd = stack.pop()
                    code(line)
                    oneline = not cline.endswith(':')
                    multiline = cmd if cline.endswith('\\') else False
                    if not oneline and not multiline:
                        stack.append(cmd)
                elif cmd == 'end' and stack:
                    code('#end(%s) %s' % (stack.pop(), line.strip()[3:]))
                elif cmd == 'include':
                    p = cline.split(None, 2)[1:]
                    if len(p) == 2:
                        code('_=_include(%s, _stdout, %s)' % (repr(p[0]), p[1]))
                    elif p:
                        code('_=_include(%s, _stdout)' % repr(p[0]))
                    else:
                        code('_printlist(_base)')
                elif cmd == 'rebase':
                    p = cline.split(None, 2)[1:]
                    if len(p) == 2:
                        code("globals()['_rebase']=(%s, dict(%s))" % (repr(p[0]), p[1]))
                    elif p:
                        code("globals()['_rebase']=(%s, {})" % repr(p[0]))
                else:
                    code(line)
            else:
                if line.strip().startswith('%%'):
                    line = line.replace('%%', '%', 1)
                ptrbuffer.append(yield_tokens(line))

        flush()
        return ('\n').join(codebuffer) + '\n'

    def subtemplate(self, _name, _stdout, *args, **kwargs):
        for dictarg in args:
            kwargs.update(dictarg)

        if _name not in self.cache:
            self.cache[_name] = self.__class__(name=_name, lookup=self.lookup)
        return self.cache[_name].execute(_stdout, kwargs)

    def execute(self, _stdout, *args, **kwargs):
        for dictarg in args:
            kwargs.update(dictarg)

        env = self.defaults.copy()
        env.update({'_stdout': _stdout, '_printlist': _stdout.extend, '_include': self.subtemplate, 
           '_str': self._str, '_escape': self._escape})
        env.update(kwargs)
        eval(self.co, env)
        if '_rebase' in env:
            (subtpl, rargs) = env['_rebase']
            subtpl = self.__class__(name=subtpl, lookup=self.lookup)
            rargs['_base'] = _stdout[:]
            del _stdout[:]
            return subtpl.execute(_stdout, rargs)
        return env

    def render(self, *args, **kwargs):
        """ Render the template using keyword arguments as local variables. """
        for dictarg in args:
            kwargs.update(dictarg)

        stdout = []
        self.execute(stdout, kwargs)
        return ('').join(stdout)


def template(*args, **kwargs):
    """
    Get a rendered template as a string iterator.
    You can use a name, a filename or a template string as first parameter.
    Template rendering arguments can be passed as dictionaries
    or directly (as keyword arguments).
    """
    tpl = args[0] if args else None
    template_adapter = kwargs.pop('template_adapter', SimpleTemplate)
    if tpl not in TEMPLATES or DEBUG:
        settings = kwargs.pop('template_settings', {})
        lookup = kwargs.pop('template_lookup', TEMPLATE_PATH)
        if isinstance(tpl, template_adapter):
            TEMPLATES[tpl] = tpl
            if settings:
                TEMPLATES[tpl].prepare(**settings)
        elif '\n' in tpl or '{' in tpl or '%' in tpl or '$' in tpl:
            TEMPLATES[tpl] = template_adapter(source=tpl, lookup=lookup, **settings)
        else:
            TEMPLATES[tpl] = template_adapter(name=tpl, lookup=lookup, **settings)
    if not TEMPLATES[tpl]:
        abort(500, 'Template (%s) not found' % tpl)
    for dictarg in args[1:]:
        kwargs.update(dictarg)

    return TEMPLATES[tpl].render(kwargs)


mako_template = functools.partial(template, template_adapter=MakoTemplate)
cheetah_template = functools.partial(template, template_adapter=CheetahTemplate)
jinja2_template = functools.partial(template, template_adapter=Jinja2Template)
simpletal_template = functools.partial(template, template_adapter=SimpleTALTemplate)

def view(tpl_name, **defaults):
    """ Decorator: renders a template for a handler.
        The handler can control its behavior like that:

          - return a dict of template vars to fill out the template
          - return something other than a dict and the view decorator will not
            process the template, but return the handler result as is.
            This includes returning a HTTPResponse(dict) to get,
            for instance, JSON with autojson or other castfilters.
    """

    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if isinstance(result, (dict, DictMixin)):
                tplvars = defaults.copy()
                tplvars.update(result)
                return template(tpl_name, **tplvars)
            return result

        return wrapper

    return decorator


mako_view = functools.partial(view, template_adapter=MakoTemplate)
cheetah_view = functools.partial(view, template_adapter=CheetahTemplate)
jinja2_view = functools.partial(view, template_adapter=Jinja2Template)
simpletal_view = functools.partial(view, template_adapter=SimpleTALTemplate)
TEMPLATE_PATH = [
 './', './views/']
TEMPLATES = {}
DEBUG = False
HTTP_CODES = httplib.responses
HTTP_CODES[418] = "I'm a teapot"
_HTTP_STATUS_LINES = dict((k, '%d %s' % (k, v)) for (k, v) in HTTP_CODES.iteritems())
ERROR_PAGE_TEMPLATE = '\n%try:\n    %from bottle import DEBUG, HTTP_CODES, request, touni\n    %status_name = HTTP_CODES.get(e.status, \'Unknown\').title()\n    <!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">\n    <html>\n        <head>\n            <title>Error {{e.status}}: {{status_name}}</title>\n            <style type="text/css">\n              html {background-color: #eee; font-family: sans;}\n              body {background-color: #fff; border: 1px solid #ddd;\n                    padding: 15px; margin: 15px;}\n              pre {background-color: #eee; border: 1px solid #ddd; padding: 5px;}\n            </style>\n        </head>\n        <body>\n            <h1>Error {{e.status}}: {{status_name}}</h1>\n            <p>Sorry, the requested URL <tt>{{repr(request.url)}}</tt>\n               caused an error:</p>\n            <pre>{{e.output}}</pre>\n            %if DEBUG and e.exception:\n              <h2>Exception:</h2>\n              <pre>{{repr(e.exception)}}</pre>\n            %end\n            %if DEBUG and e.traceback:\n              <h2>Traceback:</h2>\n              <pre>{{e.traceback}}</pre>\n            %end\n        </body>\n    </html>\n%except ImportError:\n    <b>ImportError:</b> Could not generate the error page. Please add bottle to\n    the import path.\n%end\n'
request = Request()
response = Response()
local = threading.local()
app = default_app = AppStack()
app.push()
ext = _ImportRedirect(__name__ + '.ext', 'bottle_%s').module