# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/haus/components/standard.py
# Compiled at: 2008-11-12 23:57:47
""".. _StandardFunctionsComponent:

``standard`` -- Standard Functions
==================================

Provides some baseline functions for the framework.
Really just ``routing_args``, ``routing_kwargs`` and some
do-nothings that are there to be overridden by
later-loading components. This is really just plumbing that
most users probably don't care about.

"""
from haus.components.abstract import Component, wraps

class StandardFunctionsComponent(Component):
    __module__ = __name__
    provides = [
     'get_session', 'invalidate_session', 'routing_args', 'routing_kwargs', 'get_cache', 'get_logger', 'get_config']

    def __init__(self, wrk):
        self.config = wrk.config
        wrk.functions['get_session'] = self.get_session
        wrk.functions['invalidate_session'] = self.invalidate_session
        wrk.functions['routing_args'] = self.routing_args
        wrk.functions['routing_kwargs'] = self.routing_kwargs
        wrk.functions['get_cache'] = self.get_cache
        wrk.functions['get_logger'] = self.get_logger
        wrk.functions['get_config'] = self.get_config

    def get_session(self, environ):
        return

    def invalidate_session(self, environ):
        return

    def routing_args(self, environ):
        return environ.get('wsgiorg.routing_args', ((), None))[0]

    def routing_kwargs(self, environ):
        return environ.get('wsgiorg.routing_args', (None, {}))[1]

    def get_cache(self, environ):
        return

    def get_logger(self, environ):
        return

    def get_config(self, environ):
        return self.config

    def __call__(self, wrk, *args, **kwargs):

        def middleware(app):

            @wraps(app)
            def proxy(environ, start_response):
                environ['haus.functions'] = wrk.functions
                return app(environ, start_response)

            return proxy

        return middleware