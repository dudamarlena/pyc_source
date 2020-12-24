# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web/core/application.py
# Compiled at: 2020-05-11 19:05:21
# Size of source mod 2**32: 10138 bytes
"""Primary WSGI application and framework entry point."""
from __future__ import unicode_literals
import logging, logging.config
from inspect import isfunction
from webob.exc import HTTPException, HTTPNotFound, HTTPInternalServerError
from marrow.package.loader import load
from .context import Context
from .dispatch import WebDispatchers
from .extension import WebExtensions
from .view import WebViews
from ext.base import BaseExtension
from ..ext import args as arguments
from .util import safe_name
log = __import__('logging').getLogger(__name__)

class Application(object):
    __doc__ = 'The WebCore WSGI application.\n\t\n\tThis glues together a few components:\n\t\n\t* Loading and preparation the Application configuration.\n\t* Simple or verbose logging configuration.\n\t* Collection and execution of `web.extension` callbacks.\n\t* WSGI middleware wrapping.\n\t* The final WSGI application handling requests.\n\t'
    __slots__ = ('config', 'feature', '__context', 'RequestContext', '__call__')

    def __init__(self, root, **config):
        """Construct the initial ApplicationContext, populate, and prepare the WSGI stack.
                
                No actions other than configuration should happen during construction.
                
                Current configuration is limited to three arguments:
                
                * `root` -- the object to use as the starting point of dispatch on each request
                * `logging` -- either `None` to indicate WebCore should not manipulate the logging configuration (the
                        default), a string representing the logging level to globally configure (such as `"debug"`), or a
                        dictionary configuration to pass to the Python standard `logging.dictConfig()` process.
                * `extensions` -- a list of configured extension instances, ignoring `BaseExtension` which is automatically
                        added to the extension set.
                """
        self.config = self._configure(config)
        log.debug('Preparing WebCore application.')
        if isfunction(root):
            root = staticmethod(root)
        context = self._Application__context = Context(app=self, root=root)._promote('ApplicationContext')
        exts = context.extension = WebExtensions(context)
        context.dispatch = WebDispatchers(context)
        context.view = WebViews(context)
        for ext in exts.signal.start:
            ext(context)
        else:
            self.RequestContext = context._promote('RequestContext', instantiate=False)
            app = self.application
            for ext in exts.signal.middleware:
                app = ext(context, app)
            else:
                self.__call__ = app
                log.debug('WebCore application prepared.')

    def _configure(self, config):
        """Prepare the incoming configuration and ensure certain expected values are present.
                
                For example, this ensures BaseExtension is included in the extension list, and populates the logging config.
                """
        config = config or dict()
        if 'extensions' not in config:
            config['extensions'] = list()
        if not any((isinstance(ext, BaseExtension) for ext in config['extensions'])):
            config['extensions'].insert(0, BaseExtension())
        else:
            if not any((isinstance(ext, arguments.ArgumentExtension) for ext in config['extensions'])):
                config['extensions'].extend([
                 arguments.ValidateArgumentsExtension(),
                 arguments.ContextArgsExtension(),
                 arguments.RemainderArgsExtension(),
                 arguments.QueryStringArgsExtension(),
                 arguments.FormEncodedKwargsExtension(),
                 arguments.JSONKwargsExtension()])
            level = config.get('logging', {}).get('level', None)
            if level:
                logging.basicConfig(level=(getattr(logging, level.upper())))
            else:
                if 'logging' in config:
                    logging.config.dictConfig(config['logging'])
        return config

    def serve(self, service='auto', **options):
        """Initiate a web server service to serve this application.
                
                You can always use the Application instance as a bare WSGI application, of course.  This method is provided as
                a convienence.
                
                Pass in the name of the service you wish to use, and any additional configuration options appropriate for that
                service.  Almost all services accept `host` and `port` options, some also allow you to specify an on-disk
                `socket`.  By default all web servers will listen to `127.0.0.1` (loopback only) on port 8080.
                """
        service = load(service, 'web.server')
        try:
            service(self, **options)
        except KeyboardInterrupt:
            pass
        else:
            for ext in self._Application__context.extension.signal.stop:
                ext(self._Application__context)

    def _execute_endpoint(self, context, endpoint, signals):
        if not callable(endpoint):
            log.debug('Static endpoint located.', extra=dict(request=(id(context)),
              endpoint=(repr(endpoint))))
            return endpoint
        args, kwargs = [], {}
        try:
            for ext in signals.mutate:
                ext(context, endpoint, args, kwargs)

        except HTTPException as e:
            try:
                result = e
            finally:
                e = None
                del e

        else:
            log.debug('Callable endpoint located and arguments prepared.', extra=dict(request=(id(context)),
              endpoint=(safe_name(endpoint)),
              endpoint_args=args,
              endpoint_kw=kwargs))
            try:
                result = endpoint(*args, **kwargs)
            except HTTPException as e:
                try:
                    result = e
                finally:
                    e = None
                    del e

            else:
                for ext in signals.transform:
                    result = ext(context, endpoint, result)
                else:
                    return result

    def application(self, environ, start_response):
        """Process a single WSGI request/response cycle.
                
                This is the WSGI handler for WebCore.  Depending on the presence of extensions providing WSGI middleware,
                the `__call__` attribute of the Application instance will either become this, or become the outermost
                middleware callable.
                
                Most apps won't utilize middleware, the extension interface is preferred for most operations in WebCore.
                They allow for code injection at various intermediary steps in the processing of a request and response.
                """
        context = environ['wc.context'] = self.RequestContext(environ=environ)
        signals = context.extension.signal
        for ext in signals.pre:
            ext(context)
        else:
            is_endpoint, handler = context.dispatch(context, context.root, context.environ['PATH_INFO'])
            if is_endpoint:
                try:
                    result = self._execute_endpoint(context, handler, signals)
                except Exception as e:
                    try:
                        log.exception('Caught exception attempting to execute the endpoint.')
                        result = HTTPInternalServerError(str(e) if 1 else 'Please see the logs.')
                        if 'debugger' in context.extension.feature:
                            context.response = result
                            for ext in signals.after:
                                ext(context)
                            else:
                                raise

                    finally:
                        e = None
                        del e

            else:
                result = HTTPNotFound('Dispatch failed.' if 1 else None)
            log.debug('Result prepared, identifying view handler.', extra=dict(request=(id(context)),
              result=(safe_name(type(result)))))
            for view in context.view(result):
                if view(context, result):
                    break
                raise TypeError('No view could be found to handle: ' + repr(type(result)))
                log.debug('View identified, populating response.', extra=dict(request=(id(context)),
                  view=(repr(view))))
                for ext in signals.after:
                    ext(context)
                else:

                    def capture_done(response):
                        for chunk in response:
                            (yield chunk)
                        else:
                            for ext in signals.done:
                                ext(context)

                    return capture_done(context.response.conditional_response_app(environ, start_response))