# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/test/server/component/abstract_listener_methods_test.py
# Compiled at: 2013-04-04 15:36:37
import inspect, mox
from unittest import TestCase
from muntjac.util import clsname, getSuperClass
from muntjac.ui.component import IComponent

class AbstractListenerMethodsTest(TestCase):

    def _testListenerAddGetRemove(self, testClass, eventClass, listenerClass, c=None):
        if c is None:
            c = testClass()
        mockListener1 = listenerClass()
        mockListener2 = listenerClass()
        self.verifyListeners(c, eventClass)
        self.addListener(c, mockListener1, listenerClass)
        self.verifyListeners(c, eventClass, mockListener1)
        self.addListener(c, mockListener2, listenerClass)
        self.verifyListeners(c, eventClass, mockListener1, mockListener2)
        if getSuperClass(eventClass) != object:
            self.verifyListeners(c, getSuperClass(eventClass), mockListener1, mockListener2)
        self.removeListener(c, mockListener1, listenerClass)
        self.verifyListeners(c, eventClass, mockListener2)
        self.removeListener(c, mockListener2, listenerClass)
        self.verifyListeners(c, eventClass)
        return

    def removeListener(self, c, listener, listenerClass):
        method = self.getRemoveListenerMethod(c.__class__, listenerClass)
        method(c, listener, listenerClass)

    def addListener(self, c, listener1, listenerClass):
        method = self.getAddListenerMethod(c.__class__, listenerClass)
        method(c, listener1, listenerClass)

    def getListeners(self, c, eventType):
        method = self.getGetListenersMethod(c.__class__)
        return method(c, eventType)

    def getGetListenersMethod(self, cls):
        return getattr(cls, 'getListeners')

    def getAddListenerMethod(self, cls, listenerClass):
        return getattr(cls, 'addListener')

    def getRemoveListenerMethod(self, cls, listenerClass):
        return getattr(cls, 'removeListener')

    def verifyListeners(self, c, eventClass, *expectedListeners):
        registeredListeners = self.getListeners(c, eventClass)
        self.assertEquals(len(expectedListeners), len(registeredListeners))
        self.assertEquals(sorted(expectedListeners), sorted(registeredListeners))


if __name__ == '__main__':
    import sys
    AbstractListenerMethodsTest().main(sys.argv)