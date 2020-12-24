# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/aha/dispatch/dispatcher.py
# Compiled at: 2011-03-18 02:44:08
__doc__ = '\nThe collection of fields definitions for coregeo \n\n$Id: dispatcher.py 653 2010-08-23 02:00:58Z ats $\n'
__author__ = 'Atsushi Shibata <shibata@webcore.co.jp>'
__docformat__ = 'plaintext'
__licence__ = 'BSD'
import re, logging
from inspect import ismethod
from urlparse import urlsplit
from router import get_router, get_fallback_router
import sys, os
from traceback import *
from google.appengine.api import memcache
from aha import Config
from aha.controller.util import get_controller_class

def dispatch(hnd):
    """
    A function to dispatch request to appropriate handler class
    """
    url = hnd.request.path
    r = get_router()
    route = r.match(url)
    if not route:
        fr = get_fallback_router()
        fr.match(url)
        route = fr.match(url)
        if not route:
            hnd.response.set_status(404)
            raise Exception('No route for url:%s' % url)
    ctrlname = route['controller']
    plugin = ''
    if '.' in ctrlname:
        (plugin, ctrlname) = ctrlname.split('.')
    ctrl_clz = get_controller_class(ctrlname, plugin)
    ctrl = ctrl_clz(hnd, route)
    try:
        exec 'from controller import application' in globals()
        if application.Application not in ctrl_clz.__bases__:
            ctrl_clz.__bases__ += (application.Application,)
        if hasattr(ctrl, 'application_init'):
            ctrl.application_init()
    except:
        pass

    logging.debug('URL "%s" is dispatched to: %sController#%s', url, route['controller'].capitalize(), route.get('action', 'index'))
    ctrl.config = Config()
    actionmethod = getattr(ctrl, route.get('action', 'index'), None)
    if not actionmethod or not getattr(actionmethod, '_exposed_', False):
        if not ctrl.config.debug:
            try:
                PAGE_CACHE_EXPIRE = config.page_cache_expire
            except AttributeError:
                PAGE_CACHE_EXPIRE = 3600
            else:
                p = urlsplit(hnd.request.url)[2]
                memcache.set(p, 'error', PAGE_CACHE_EXPIRE)
                logging.debug('%s is cahed as a error page' % p)
        ctrl.response.set_status(404)
        m = '%s %s (Method not found)'
        raise Exception(m % ctrl.response._Response__status)
    if ctrl.before_action() != False:
        if ismethod(actionmethod):
            actionmethod()
        else:
            actionmethod()
        ctrl.after_action()
    st = ctrl.response._Response__status[0]
    if st >= 400:
        raise Exception('%s %s' % ctrl.response._Response__status)
    if not ctrl.has_rendered and not ctrl.has_redirected:
        ctrl.render(template=route['action'], values=ctrl.__dict__)
    ctrl.put_cookies()
    return