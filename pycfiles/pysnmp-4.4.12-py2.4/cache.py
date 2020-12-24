# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp/proto/secmod/cache.py
# Compiled at: 2019-08-18 17:24:05
from pysnmp import nextid
from pysnmp.proto import error

class Cache(object):
    __module__ = __name__
    __stateReference = nextid.Integer(16777215)

    def __init__(self):
        self.__cacheEntries = {}

    def push(self, **securityData):
        stateReference = self.__stateReference()
        self.__cacheEntries[stateReference] = securityData
        return stateReference

    def pop(self, stateReference):
        if stateReference in self.__cacheEntries:
            securityData = self.__cacheEntries[stateReference]
        else:
            raise error.ProtocolError('Cache miss for stateReference=%s at %s' % (stateReference, self))
        del self.__cacheEntries[stateReference]
        return securityData