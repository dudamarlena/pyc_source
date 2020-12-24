# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/weborg/config/routing.py
# Compiled at: 2011-07-12 23:03:46
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
    map.explicit = False
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')
    map.connect('entries', '/entries/index.{format}', controller='entries', action='index', conditions=dict(method=['GET']))
    map.connect('entries', '/entries/{id}.{format}', controller='entries', action='show', conditions=dict(method=['GET']))
    map.connect('entries', '/entries/{id}.{format}', controller='entries', action='create', conditions=dict(method=['POST']))
    map.connect('entries', '/entries/{id}.{format}', controller='entries', action='update', conditions=dict(method=['PUT']))
    map.connect('entries', '/entries/{id}.{format}', controller='entries', action='delete', conditions=dict(method=['DELETE']))
    map.connect('entries', '/entries/{id}/new.{format}', controller='entries', action='new', conditions=dict(method=['GET']))
    map.connect('entries', '/entries/{id}/edit.{format}', controller='entries', action='edit', conditions=dict(method=['GET']))
    return map