# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pycrud/config/routing.py
# Compiled at: 2008-06-20 03:40:59
__doc__ = 'Routes configuration\n\nThe more specific and detailed routes should be defined first so they\nmay take precedent over the more generic routes. For more information\nrefer to the routes manual at http://routes.groovie.org/docs/\n'
from pylons import config
from routes import Mapper

def make_map():
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'], always_scan=config['debug'])
    map.connect('error/:action/:id', controller='error')
    map.connect(':controller/:action/:id')
    map.connect('*url', controller='template', action='index')
    map.connect('', controller='template', action='index')
    map.connect('index.html', controller='template', action='index')
    return map