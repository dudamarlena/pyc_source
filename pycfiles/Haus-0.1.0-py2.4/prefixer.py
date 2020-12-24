# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/haus/components/prefixer.py
# Compiled at: 2008-11-12 23:57:47
""".. _PrefixerComponent:

``prefixer`` -- Prefix Normalizer
=================================

This somewhat hackish component normalizes the consumption
of the path prefix (the mount point of the applicaiton, 
if you will) from ``environ['PATH_INFO']`` into ``environ['SCRIPT_NAME']``.

"""
from haus.components.abstract import Component, wraps

class PrefixerComponent(Component):
    """Consume the prefix is if seems to be unconsumed."""
    __module__ = __name__

    def __init__(self, wrk):
        self.prefix = wrk.config.get('app', {}).get('prefix', '')

    def __call__(self, wrk, *args, **kwargs):

        def middleware(app):

            @wraps(app)
            def proxy(environ, start_response):
                if not environ['SCRIPT_NAME'].endswith(self.prefix) and environ['PATH_INFO'].startswith(self.prefix):
                    environ['PATH_INFO'] = environ['PATH_INFO'][len(self.prefix):]
                    environ['SCRIPT_NAME'] += self.prefix
                return app(environ, start_response)

            return proxy

        return middleware