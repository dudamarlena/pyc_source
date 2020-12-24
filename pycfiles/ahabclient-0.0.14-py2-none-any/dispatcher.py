# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/microne/dispatcher.py
# Compiled at: 2011-03-28 04:01:43
__author__ = 'Atsushi Shibata <shibata@webcore.co.jp>'
__docformat__ = 'plaintext'
__licence__ = 'BSD'
__all__ = [
 'dispatch']
from inspect import getargspec
import logging

def dispatch(hnd):
    """
    A function to dispatch request to appropriate handler function.
    It receive hander object which has request/response object.
    The dispatcher uses route to determine which controller is needed for
    the request, passes them to appropriate hander.
    This function internally called by wsgi application.
    """
    from aha.dispatch.router import get_router
    from plugin.microne.app import Microne
    url = hnd.request.path
    r = get_router()
    route = r.match(url)
    if route:
        func = route['controller']
        (args, varargs, varkw, defaults) = getargspec(func)
        Microne.set_handler(hnd, route)
        Microne.get_controller()
        if len(args) == 1:
            route['controller'](hnd)
        else:
            route['controller']()
        Microne.controller.put_cookies()
        Microne.clear_controller()
    else:
        hnd.response.set_status(404)
        raise Exception('No route for url:%s' % url)