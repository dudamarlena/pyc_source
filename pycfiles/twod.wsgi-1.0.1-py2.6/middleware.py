# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twod/wsgi/middleware.py
# Compiled at: 2011-06-28 10:17:42
"""
WSGI and Django middleware.

"""
__all__ = ('RoutingArgsMiddleware', )

class RoutingArgsMiddleware(object):
    """
    Django middleware which implements the `wsgiorg.routing_args standard
    <http://wsgi.org/wsgi/Specifications/routing_args>`_.
    
    """

    def process_view(self, request, view_func, view_args, view_kwargs):
        request.environ['wsgiorg.routing_args'] = (
         view_args, view_kwargs.copy())