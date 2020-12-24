# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp/entity/observer.py
# Compiled at: 2019-08-18 17:24:05
from pysnmp import error

class MetaObserver(object):
    """This is a simple facility for exposing internal SNMP Engine
       working details to pysnmp applications. These details are
       basically local scope variables at a fixed point of execution.

       Two modes of operations are offered:
       1. Consumer: app can request an execution point context by execution point ID.
       2. Provider: app can register its callback function (and context) to be invoked
          once execution reaches specified point. All local scope variables
          will be passed to the callback as in #1.

       It's important to realize that execution context is only guaranteed
       to exist to functions that are at the same or deeper level of invocation
       relative to execution point specified.
    """
    __module__ = __name__

    def __init__(self):
        self.__observers = {}
        self.__contexts = {}
        self.__execpoints = {}

    def registerObserver(self, cbFun, *execpoints, **kwargs):
        if cbFun in self.__contexts:
            raise error.PySnmpError('duplicate observer %s' % cbFun)
        else:
            self.__contexts[cbFun] = kwargs.get('cbCtx')
        for execpoint in execpoints:
            if execpoint not in self.__observers:
                self.__observers[execpoint] = []
            self.__observers[execpoint].append(cbFun)

    def unregisterObserver(self, cbFun=None):
        if cbFun is None:
            self.__observers.clear()
            self.__contexts.clear()
        else:
            for execpoint in dict(self.__observers):
                if cbFun in self.__observers[execpoint]:
                    self.__observers[execpoint].remove(cbFun)
                if not self.__observers[execpoint]:
                    del self.__observers[execpoint]

        return

    def storeExecutionContext(self, snmpEngine, execpoint, variables):
        self.__execpoints[execpoint] = variables
        if execpoint in self.__observers:
            for cbFun in self.__observers[execpoint]:
                cbFun(snmpEngine, execpoint, variables, self.__contexts[cbFun])

    def clearExecutionContext(self, snmpEngine, *execpoints):
        if execpoints:
            for execpoint in execpoints:
                del self.__execpoints[execpoint]

        else:
            self.__execpoints.clear()

    def getExecutionContext(self, execpoint):
        return self.__execpoints[execpoint]