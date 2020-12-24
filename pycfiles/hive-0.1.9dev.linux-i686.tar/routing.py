# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/git/lib/python2.5/site-packages/hive/config/routing.py
# Compiled at: 2011-07-08 01:47:53
"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from hive.lib.routes import Mapper

def make_map(config):
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'], always_scan=config['debug'])
    map.minimization = False
    map.explicit = False
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')
    map.resource('user', 'users')
    map.resource('repo', 'repos')
    map.resource('rule', 'rules', parent_resource=dict(member_name='repo', collection_name='repos'), name_prefix='')
    map.resource('group', 'groups', parent_resource=dict(member_name='repo', collection_name='repos'), name_prefix='')
    return map