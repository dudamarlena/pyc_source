# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysvnmanager/config/routing.py
# Compiled at: 2010-08-08 03:18:44
"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from routes import Mapper

def make_map(config):
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'], always_scan=config['debug'])
    map.minimization = False
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')
    map.connect('home', '/', controller='check', action='index')
    map.connect('login', '/login', controller='security', action='index')
    map.connect('logout', '/logout', controller='security', action='logout')
    map.connect('/{controller}', action='index')
    map.connect('/{controller}/{action}')
    map.connect('/{controller}/{action}/{id}')
    map.explicit = True
    return map