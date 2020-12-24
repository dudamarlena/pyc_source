# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/site-packages/canteen/core/runtime.py
# Compiled at: 2015-01-05 19:41:29
__doc__ = '\n\n  core runtime\n  ~~~~~~~~~~~~\n\n  platform internals and logic to discover/load/inject.\n\n  :author: Sam Gammon <sg@samgammon.com>\n  :copyright: (c) Sam Gammon, 2014\n  :license: This software makes use of the MIT Open Source License.\n            A copy of this license is included as ``LICENSE.md`` in\n            the root of the project.\n\n'
from __future__ import print_function
import os, sys, abc, inspect, importlib, threading
from .meta import Proxy
from .injection import Bridge
__runtime__ = threading.local()

class Runtime(object):
    """ Describes a structure that can manage and schedule execution for Canteen
      applications. When a Canteen app is running, there is always an active
      ``Runtime`` object behind it.

      One ``Runtime`` is active per thread at-at-time. It is not possible to use
      different ``Runtime`` classes concurrently (for instance, uWSGI and PyPy),
      but runtimes can be composed into a compound structure that expresses
      combined functionality. """
    routes = None
    config = None
    bridge = None
    application = None
    __hooks__ = {}
    __owner__ = 'Runtime'
    __wrapped__ = None
    __singleton__ = False
    __metaclass__ = Proxy.Component
    __precedence__ = False
    precedence = property(lambda self: self.__precedence__)

    @staticmethod
    def base_exception():
        """  """
        return False

    @classmethod
    def spawn(cls, app):
        """  """
        global __runtime__
        if not getattr(__runtime__, 'active', None):
            __runtime__.active = (cls.resolve() if cls is Runtime else cls)(app)
        return __runtime__.active

    @classmethod
    def resolve(cls):
        """  """
        _default, _preferred = None, []
        for child in cls.iter_children():
            if hasattr(child, '__default__') and child.__default__:
                _default = child
                continue
            _preferred.append(child)

        for item in _preferred:
            if item.__precedence__:
                return item

        if _preferred:
            return _preferred[0]
        else:
            return _default

    @classmethod
    def set_precedence(cls, status=False):
        """  """
        return setattr(cls, '__precendence__', status) or cls

    @classmethod
    def add_hook(cls, hook, context_and_func):
        """  """
        context, func = context_and_func
        assert isinstance(hook, basestring), 'hook name must be a string'
        if hook not in cls.__hooks__:
            cls.__hooks__[hook] = []
        cls.__hooks__[hook].append((context, func))
        return cls

    @classmethod
    def get_hooks(cls, point):
        """  """
        if point in cls.__hooks__:
            for i in cls.__hooks__[point]:
                yield i

        raise StopIteration()

    @classmethod
    def execute_hooks(cls, points, *args, **kwargs):
        """  """
        if isinstance(points, basestring):
            points = (points,)
        for point in points:
            for context, hook in cls.get_hooks(point):
                try:
                    if isinstance(hook, classmethod):
                        hook.__func__(context, *args, **kwargs)
                    elif isinstance(hook, staticmethod):
                        hook.__func__(*args, **kwargs)
                    else:
                        if not (hasattr(context, '__singleton__') or not context.__singleton__):
                            raise RuntimeError('Cannot execute hook method "%s" without matching singleton context.' % hook)
                        obj = Proxy.Component.singleton_map.get(context.__name__)
                        if not obj:
                            raise RuntimeError('No matching singleton for hook method "%s".' % hook)
                        hook(point, obj, *args, **kwargs)
                except Exception:
                    raise

    def __init__(self, app):
        """  """
        self.application, self.bridge = app, Bridge()

    def initialize(self):
        """  """
        self.execute_hooks('initialize', runtime=self)

    def configure(self, config):
        """  """
        self.config = config
        self.initialize()
        return self

    def serve(self, interface, port, bind_only=False):
        """  """
        server = self.bind(interface, port)
        if bind_only:
            return server
        try:
            server.serve_forever()
        except (KeyboardInterrupt, Exception):
            print('Exiting.')
            sys.exit(0)

    def bind_environ(self, environ):
        """  """
        from ..logic import http
        self.routes = http.HTTPSemantics.route_map.bind_to_environ(environ)
        return (
         http.HTTPSemantics,
         http.HTTPSemantics.new_request(environ),
         http.HTTPSemantics.new_response())

    def handshake(self, key, origin=None):
        """ WIP """
        raise NotImplementedError('Runtime "%s" does not support realtime dispatch semantics. ' % self)

    def send(self, payload, binary=False):
        """ WIP """
        raise NotImplementedError('Runtime "%s" does not support realtime dispatch semantics. ' % self)

    def send(self):
        """ WIP """
        raise NotImplementedError('Runtime "%s" does not support realtime dispatch semantics. ' % self)

    def receive(self):
        """ WIP """
        raise NotImplementedError('Runtime "%s" does not support realtime dispatch semantics. ' % self)

    def dispatch(self, environ, start_response):
        """ WIP """
        from ..base import handler as base_handler
        context = {'environ': environ, 
           'start_response': start_response, 
           'runtime': self}
        self.execute_hooks('dispatch', **context)
        http, request, response = context['http'], context['request'], context['response'] = self.bind_environ(environ)
        self.execute_hooks('request', **context)
        endpoint, arguments = context['endpoint'], context['arguments'] = self.routes.match()
        self.execute_hooks('match', **context)
        handler = context['handler'] = http.resolve_route(endpoint)
        if not handler:
            context.update({'code': 404, 
               'error': True, 
               'exception': None, 
               'response': None})
            self.execute_hooks(('error', 'complete'), **context)
            http.error(404)
        if isinstance(handler, type) and issubclass(handler, base_handler.Handler):
            flow = context['handler'] = handler(**context)
            self.execute_hooks('handler', **context)
            result, iterator = flow(arguments), None
            if isinstance(result, tuple) and len(result) == 2:
                iterator, result = result
            elif isinstance(result, tuple) and len(result) == 4:
                status, headers, content_type, content = context['status'], context['headers'], context['content_type'], context['content'] = result
                _response = context['response'] = response.__class__(content, **{'status': status, 
                   'headers': headers, 
                   'mimetype': content_type})
                self.execute_hooks(('response', 'complete'), **context)
                return _response(environ, start_response)
            status, headers, content_type, content = context['status'], context['headers'], context['content_type'], context['content'] = (
             result.status, result.headers, result.content_type, result.response)
            self.execute_hooks(('response', 'complete'), **context)
            start_response(result.status, [ (k.encode('utf-8').strip(), v.encode('utf-8').strip()) for k, v in result.headers
                                          ])
            return iterator or result.response
        else:
            if isinstance(handler, type) or callable(handler):

                def _foreign_runtime_bridge(status, headers):
                    """  """
                    context['status'], context['headers'], context['response'] = status, headers, None
                    self.execute_hooks(('response', 'complete'), **context)
                    return start_response(status, headers)

                _foreign_runtime_bridge.runtime = self
                _foreign_runtime_bridge.arguments = arguments
                _foreign_runtime_bridge.start_response = start_response
                context['start_response'] = _foreign_runtime_bridge
                self.execute_hooks('handler', **context)
                return handler(environ, _foreign_runtime_bridge)
            if inspect.isfunction(handler):
                for prop, val in (
                 (
                  'runtime', self),
                 (
                  'self', self.bridge),
                 (
                  'arguments', arguments),
                 (
                  'request', request),
                 (
                  'response', response),
                 (
                  'environ', environ),
                 (
                  'start_response', start_response),
                 (
                  'Response', response.__class__)):
                    handler.__globals__[prop] = val

                self.execute_hooks('handler', **context)
                result = context['response'] = handler(**arguments)
                if isinstance(result, response.__class__):
                    context['headers'], context['content'] = result.headers, result.response
                    self.execute_hooks(('response', 'complete'), **context)
                    return response(environ, start_response)
                if isinstance(result, tuple):
                    if len(result) == 2:
                        status, response = context['status'], context['response'] = result
                        headers = context['headers'] = [
                         ('Content-Type', 'text/html; charset=utf-8')]
                        self.execute_hooks(('response', 'complete'), **context)
                        start_response(status, headers)
                        return iter([response])
                    if len(result) == 3:
                        status, headers, response = context['status'], context['headers'], context['response'] = result
                        if isinstance(headers, dict):
                            headers = headers.items()
                            if 'Content-Type' not in headers:
                                headers['Content-Type'] = context['headers']['Content-Type'] = 'text/html; charset=utf-8'
                        self.execute_hooks(('response', 'complete'), **context)
                        start_response(status, headers)
                        return iter([response])
                elif isinstance(result, basestring):
                    status, headers = context['status'], context['headers'], context['response'] = (
                     '200 OK', [('Content-Type', 'text/html; charset=utf-8')])
                    self.execute_hooks(('response', 'complete'), **context)
                    start_response(status, headers)
                    return iter([result])
            if not callable(handler):
                if isinstance(handler, basestring):
                    context['status'], context['headers'], context['response'] = '200 OK', [('Content-Type', 'text/html; charset=utf-8')], result
                    self.execute_hooks(('response', 'complete'), **context)
                    return iter([handler])
            raise RuntimeError('Unrecognized handler type: "%s".' % type(handler))
            return

    def wrap(self, dispatch):
        """  """
        if not self.__wrapped__:
            _dispatch = dispatch
            dev_config = getattr(self.config, 'app', {}).get('dev', {})
            if 'profiler' in dev_config:
                profiler_cfg = dev_config['profiler']
                if profiler_cfg.get('enable', False):
                    try:
                        import cProfile as profile
                    except ImportError:
                        import profile

                    profile_path = profiler_cfg.get('dump_file', os.path.abspath(os.path.join(*(os.getcwd(), '.develop', 'app.profile'))))
                    pkwargs = profiler_cfg.get('profile_kwargs', {})
                    _current_profile = profile.Profile(**pkwargs)
                    if profiler_cfg.get('on_request', True):

                        def maybe_flush_profile():
                            """  """
                            _current_profile.dump_stats(profile_path)

                    else:
                        raise RuntimeError('Cross-request profiling is currently unsupported.')

                    def _dispatch(*args, **kwargs):
                        """ Wrapper to enable profiler support. """
                        response = _current_profile.runcall(dispatch, *args, **kwargs)
                        maybe_flush_profile()
                        return response

            self.__wrapped__ = _dispatch
        return self.__wrapped__

    def bind(self, interface, port):
        """  """
        raise NotImplementedError

    def callback(self, start_response):
        """  """

        def responder(status, headers):
            """  """
            return start_response(status, headers)

        return responder

    def __call__(self, environ, start_response):
        """  """
        try:
            return self.wrap(self.dispatch)(environ, self.callback(start_response))
        except self.base_exception as exc:
            return exc(environ, start_response)
        except Exception:
            raise


class Library(object):
    """ Provides a structure that can be used to indicate (and safely handle)
      external dependencies. Used extensively inside Canteen and usable by app
      developers to introduce different functionality depending on the packages
      available. """
    name = None
    strict = False
    package = None
    exception = None
    supported = None
    __owner__, __metaclass__ = 'Library', Proxy.Component

    def __init__(self, package, strict=False):
        """ Initialize this ``Library`` with a target Python ``package``, and
        optionally ``strict`` mode.

        :param package: ``str`` path to a package that should be imported. When
          ``Library`` is used in a ``with`` block, the library import must be
          successful to proceed in loading/processing the contents of the
          block.

        :param strict: ``bool`` flag to indicate that the developer wishes to
          hard-fail if the given ``package`` is not available. Defaults to
          ``False``, meaning any ``ImportError`` encountered loading ``package``
          will simply be ignored. ``True`` causes the exception to bubble to the
          caller. """
        if isinstance(package, basestring):
            self.name = package
        elif isinstance(package, type(abc)):
            self.name, self.package, self.supported = package.__name__, package, True
        self.strict = strict

    def load(self, *subpackages):
        """ Load a subpackage from an already-constructed/resolved ``Library``
        object. This is usually used from the ``library`` element in a ``with``
        block.

        :param subpackages: Positional arguments are loaded as subpackages/
          submodules from the original ``package`` passed during construciton.
          For instance, ``Library('collections').load('defaultdict')`` is
          essentially equivalent to ``from collections import defaultdict``.

        :raises ImportError: Import issues are directly surfaced from this
          method, as it is designed to be wrapped in a ``with`` block.

        :returns: Loaded ``module`` object. """
        loaded = []
        for package in subpackages:
            loaded.append(importlib.import_module(('.').join((self.name, package))))

        if len(loaded) == 1:
            return loaded[0]
        return tuple(loaded)

    def __enter__(self):
        """ Context entrance method, responsible for triggering a load of the top-
        level package and propagating exceptions if ``strict`` mode is active.

        :retunrs: ``tuple`` of the form ``(self, package)``, such that it can
          be unpacked into ``(library, package)`` in a ``with ... as``
          block. """
        if not self.package and self.supported is None:
            try:
                self.package = importlib.import_module(self.name)
            except ImportError as e:
                self.supported, self.exception = False, e
                if self.strict:
                    raise
            else:
                self.supported = True

        return (
         self, self.package)

    def __exit__(self, exception_cls, exception, traceback):
        """  """
        if exception:
            if self.strict:
                return False
        return True