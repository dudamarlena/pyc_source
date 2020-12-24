# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.5.0-Power_Macintosh/egg/workspace/plugins/items.py
# Compiled at: 2006-04-03 07:45:33
from zope.interface import Interface, Attribute, implements
import sprinkles
from workspace.interfaces import IWorkspaceSection
from workspace.plugins.items_interfaces import IWorkspaceItem

class ItemsSection(object):
    __module__ = __name__
    implements(IWorkspaceSection)
    data = []
    name = 'items'

    def __init__(self):
        self.types = sprinkles.fromPackage('workspace.plugins', IWorkspaceItem.implementedBy)

    def append(self, i):
        self.data.append(i)

    @classmethod
    def fromSystem(cls):
        self = cls()
        for t in self.types:
            d = t.fromSystem()
            for x in d:
                self.append(x)

        return self

    @classmethod
    def canHandle(cls, name):
        if name == cls.name:
            return True
        return False

    def getItem(self, l):
        if type(l) is type(''):
            name = l.split(':')[0]
            for t in self.types:
                if t.name == name:
                    return t.unserialize(l)

        return