# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/cache/metaconfigure.py
# Compiled at: 2007-12-05 09:41:22
"""
"""
__docformat__ = 'restructuredtext'
from zope.app.component.metaconfigure import utility
from iw.cache.interfaces import IIWMemcachedClient
from iw.cache.memcached import IWMemcachedClient
from iw.cache.memcached import NS as memcached_ns
from iw.cache.interfaces import IIWRAMCache
from iw.cache.ramcache import IWRAMCache
from iw.cache.ramcache import NS as ramcache_ns

def memcachedserver(_context, server=None, name=None, maxage=None):
    if name is None:
        name = NS
    if maxage is None:
        maxage = 3600
    if server is None:
        servers = [
         '127.0.0.1:11211']
    else:
        servers = [
         str(server)]
    component = IWMemcachedClient(servers=servers, defaultNS=name, defaultAge=maxage)
    utility(_context, provides=IIWMemcachedClient, component=component, name=name)
    return


def ramcache(_context, name=None, maxage=None):
    if name is None:
        name = NS
    if maxage is None:
        maxage = 3600
    component = IWRAMCache(ns=name, maxAge=maxage)
    utility(_context, provides=IIWRAMCache, component=component, name=name)
    return