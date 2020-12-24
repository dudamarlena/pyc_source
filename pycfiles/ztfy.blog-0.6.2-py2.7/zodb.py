# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/blog/zodb.py
# Compiled at: 2013-02-17 05:42:39
__docformat__ = 'restructuredtext'
from BTrees.OOBTree import OOBTree
from persistent.list import PersistentList
from zodbbrowser.interfaces import IObjectHistory
from zodbbrowser.state import GenericState
from zope.component import adapts
from ztfy.blog.ordered import OrderedContainer

class OrderedContainerState(GenericState):
    """Convenient access to an OrderedContainer's items"""
    adapts(OrderedContainer, dict, None)

    def listItems(self):
        container = OrderedContainer()
        container.__setstate__(self.state)
        old_data_state = IObjectHistory(container._data).loadState(self.tid)
        old_order_state = IObjectHistory(container._order).loadState(self.tid)
        container._data = OOBTree()
        container._data.__setstate__(old_data_state)
        container._order = PersistentList()
        container._order.__setstate__(old_order_state)
        return container.items()