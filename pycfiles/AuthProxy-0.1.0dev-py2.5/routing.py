# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/authproxy/config/routing.py
# Compiled at: 2005-08-12 12:00:38
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
    map.connect('error/:action/:id', controller='error')
    auth_path = config.get('authproxy.url', 'auth')
    map.connect(auth_path, controller='auth')
    map.resource('admin', 'auth_user', controller='admin/auth_user', path_prefix='/admin', name_prefix='admin_')
    map.resource('admin', 'auth_permission', controller='admin/auth_permission', path_prefix='/admin', name_prefix='admin_')
    map.connect(':controller/:action/:id')
    map.connect('*url', controller='template', action='view')
    return map