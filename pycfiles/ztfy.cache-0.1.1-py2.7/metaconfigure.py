# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/cache/metaconfigure.py
# Compiled at: 2012-06-11 15:33:55
from ztfy.cache.metadirectives import ICacheProxyHandlerBase
from zope.component.security import PublicPermission
from zope.component.zcml import utility
from ztfy.cache.utility import CacheProxyHandler

def cache_handler(context, name='', cache_interface=None, cache_name=None):
    """Register cache proxy from ZCML"""
    handler = CacheProxyHandler(name, cache_interface, cache_name)
    utility(context, ICacheProxyHandlerBase, component=handler, permission=PublicPermission, name=name)