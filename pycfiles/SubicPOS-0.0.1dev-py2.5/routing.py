# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/subicpos/config/routing.py
# Compiled at: 2008-05-24 09:57:48
"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from pylons import config
from routes import Mapper

def make_map():
    """Create, configure and return the routes Mapper"""
    base_url = config['base_url']
    map = Mapper(directory=config['pylons.paths']['controllers'], always_scan=config['debug'])
    map.connect('error/:action/:id', controller='error')
    map.connect('%s/error/:action/:id' % base_url, controller='error')
    map.connect(':controller/:action/:id')
    map.connect('*url', controller='template', action='view')
    map.connect('%s/*url' % base_url, controller='template', action='view')
    return map