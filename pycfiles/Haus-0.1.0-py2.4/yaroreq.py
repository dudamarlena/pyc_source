# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/haus/components/yaroreq.py
# Compiled at: 2008-11-14 02:47:19
""".. _RequestObject:

==========================
``yaro`` -- Request Object
==========================

This request object generating component uses
Yaro_ to provide a (hopefully) tidy API to 
implement your application against. In addition
to Yaro's usual attributes, the request object
provides the following:

=============== ==============================
``session``     Dict of session data.
``logger``      The application logger.
``cache``       The cache manager for the app.
``loc``         Application locations.
``ff``          Dict of framework functions.
``config``      The application config.
``args``        WSGI routing args.
``vars``        WSGI routing kwargs.
=============== ==============================

.. _Yaro: http://lukearno.com/projects/yaro/

"""
from yaro import Yaro
from haus.components.abstract import Component, update_wrapper

class YaroComponent(Component):
    __module__ = __name__
    consumes = [
     'get_session', 'get_cache', 'get_logger', 'get_locaitons', 'routing_args', 'routing_kwargs']

    def __call__(self, wrk, *args, **kwargs):

        def middleware(app):
            new = Yaro(app, [('session', wrk.functions['get_session']), ('logger', wrk.functions['get_logger']), ('cache', wrk.functions['get_cache']), ('loc', wrk.functions['get_locations']),
             ('ff',
              lambda e: wrk.functions),
             ('config',
              lambda e: wrk.config), ('args', wrk.functions['routing_args']), ('vars', wrk.functions['routing_kwargs'])])
            new.__name__ = app.__name__
            return new

        return middleware