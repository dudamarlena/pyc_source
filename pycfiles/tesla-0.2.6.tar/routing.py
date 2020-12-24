# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danjac/petprojects/tesla/tests/output/ProjectName/projectname/config/routing.py
# Compiled at: 2007-09-06 07:54:15
"""Routes configuration

The more specific and detailed routes should be defined first so they may take
precedent over the more generic routes. For more information refer to the
routes manual at http://routes.groovie.org/docs/
"""
from pylons import config
from routes import Mapper

def make_map():
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'], always_scan=config['debug'])
    map.connect('error/:action/:id', controller='error')
    map.connect(':controller/:action/:id')
    map.connect('*url', controller='template', action='view')
    return map