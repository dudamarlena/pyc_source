# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/zc/shortcut/shortcut.py
# Compiled at: 2006-12-07 13:02:03
"""shortcut class

$Id$
"""
import persistent
from zope import interface
from zope.location.interfaces import ILocation
from zc.shortcut import interfaces, proxy

class Shortcut(persistent.Persistent):
    __module__ = __name__
    interface.implements(interfaces.IShortcut, ILocation)

    def __init__(self, target):
        self.__parent__ = None
        self.__name__ = None
        self.raw_target = target
        return

    @property
    def target(self):
        target = self.raw_target
        return proxy.TargetProxy(target, self.__parent__, self.__name__, self)