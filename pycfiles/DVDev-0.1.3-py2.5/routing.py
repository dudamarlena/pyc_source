# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/dvdev/config/routing.py
# Compiled at: 2009-04-17 21:15:04
"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from pylons import config
from routes import Mapper
from os import path

def make_map():
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'], always_scan=config['debug'])
    map.minimization = False
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')
    default_repo = config.get('repo', '').split()[0]
    default_controller = config.get('project_home', '').split()[0]
    repoid = default_repo.split(path.sep)[(-1)]
    map.connect('/source', controller='mercurialgateway', path_info='')
    map.connect('source', '/source/{path_info:.*}', controller='mercurialgateway')
    map.connect('/wiki', controller='wiki', action='view', repository=repoid, wikipath='')
    map.connect('/wiki/', controller='wiki', action='view', repository=repoid, wikipath='')
    map.connect('/wiki/{action}/*wikipath', controller='wiki', repository=repoid, action='view')
    map.connect('/{repository}/wiki', controller='wiki', action='view', wikipath='')
    map.connect('/{repository}/wiki/', controller='wiki', action='view', wikipath='')
    map.connect('wiki', '/{repository}/wiki/{action}/*wikipath', controller='wiki', action='view', wikipath='')
    map.connect('/login', controller='openiduser', action='login')
    map.connect('/success', controller='openiduser', action='success')
    map.connect('/{repository}/dv/revert/*filepath', controller='dv', action='revert')
    map.connect('/', repository=repoid, controller=default_controller, action='index')
    map.connect('/{repository}', controller=default_controller, action='index')
    map.connect('/{repository}/{controller}', action='index')
    map.connect('/{repository}/{controller}/{action}')
    map.connect('/{repository}/{controller}/{action}/{id}')
    return map