# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/quickwiki/config/routing.py
# Compiled at: 2009-02-23 12:50:50
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
    map.connect('home', '/', controller='pages', action='show', title='FrontPage')
    map.connect('pages', '/pages', controller='pages', action='index')
    map.connect('show_page', '/pages/show/{title}', controller='pages', action='show')
    map.connect('edit_page', '/pages/edit/{title}', controller='pages', action='edit')
    map.connect('save_page', '/pages/save/{title}', controller='pages', action='save', conditions=dict(method='POST'))
    map.connect('delete_page', '/pages/delete', controller='pages', action='delete')
    map.connect('/{title}', controller='pages', action='show')
    return map