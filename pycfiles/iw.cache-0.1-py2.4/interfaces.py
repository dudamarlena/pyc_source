# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/cache/interfaces.py
# Compiled at: 2007-12-05 09:41:22
"""
cache interfaces
"""
__docformat__ = 'restructuredtext'
from zope.interface import Interface

class IWCache(Interface):
    """ marker interface for IWCaches
    """
    __module__ = __name__


class IIWMemcachedClient(IWCache):
    __module__ = __name__


class IIWRAMCache(IWCache):
    __module__ = __name__


class MemcachedError(Exception):
    """exception for memcached server
    """
    __module__ = __name__