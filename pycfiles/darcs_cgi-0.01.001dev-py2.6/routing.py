# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/darcscgi/config/routing.py
# Compiled at: 2009-09-11 13:58:44
"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from pylons import config
from routes import Mapper

def make_map():
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'], always_scan=config['debug'])
    map.minimization = False
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')
    map.connect('/stylesheets/{sheet}', controller='template', action='stylesheets')
    map.connect('/', controller='information', action='redirect')
    map.connect('/_information', controller='information', action='redirect')
    map.connect('/_information/', controller='information', action='redirect')
    map.connect('/_information/{action}', controller='information')
    map.connect('/{repository}', controller='repositories', action='patch_wrapper')
    map.connect('/{repository}/', controller='repositories', action='patch_wrapper')
    map.connect('/{repository}/*path', controller='repositories', action='fetch_wrapper')
    map.connect('/{controller}/{action}')
    map.connect('/{controller}/{action}/{id}')
    return map