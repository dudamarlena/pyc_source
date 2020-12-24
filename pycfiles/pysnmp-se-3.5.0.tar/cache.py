# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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