# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/blog/ordered.py
# Compiled at: 2013-02-17 05:41:57
__docformat__ = 'restructuredtext'
from BTrees.OOBTree import OOBTree
from persistent.list import PersistentList
from ztfy.skin.interfaces import IOrderedContainer
from zope.container.ordered import OrderedContainer as OrderedContainerBase
from zope.interface import implements
from zope.traversing.api import getName

class OrderedContainer(OrderedContainerBase):
    implements(IOrderedContainer)

    def __init__(self):
        self._data = OOBTree()
        self._order = PersistentList()

    def updateOrder(self, order, iface=None):
        if iface is not None:
            order = [ id for id in order if iface.providedBy(self[id]) ] + [ getName(i) for i in self.values() if not iface.providedBy(i) ]
        else:
            order = order + [ k for k in self.keys() if k not in order ]
        super(OrderedContainer, self).updateOrder(order)
        return

    def moveUp(self, id):
        keys = list(self.keys())
        index = keys.index(id)
        if index > 0:
            keys[index - 1], keys[index] = keys[index], keys[(index - 1)]
            self.context.updateOrder(keys)

    def moveDown(self, id):
        keys = list(self.keys())
        index = keys.index(id)
        if index < len(keys) - 1:
            keys[index + 1], keys[index] = keys[index], keys[(index + 1)]
            self.context.updateOrder(keys)

    def moveFirst(self, id):
        keys = list(self.keys())
        index = keys.index(id)
        if index > 0:
            keys = keys[index:index + 1] + keys[:index] + keys[index + 1:]
            self.updateOrder(keys)

    def moveLast(self, id):
        keys = list(self.keys())
        index = keys.index(id)
        if index < len(keys) - 1:
            keys = keys[:index] + keys[index + 1:] + keys[index:index + 1]
            self.context.updateOrder(keys)