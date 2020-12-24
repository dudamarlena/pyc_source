# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/interfaces/item.py
# Compiled at: 2008-06-20 09:35:25
from zope.interface import Interface

class IItemManagement(Interface):
    """Provides methods to manage item content objects.
    """
    __module__ = __name__

    def addItem(product, amount=1):
        """Adds a item.
        """
        pass

    def addItemsFromCart(cart):
        """At the items from another Cart.
        """
        pass

    def deleteItemByOrd(ord):
        """Deletes the item by passed ord.
        """
        pass

    def deleteItem(id):
        """Deletes item with passed id.
        """
        pass

    def getItem(id):
        """Returns item with passed id.
        """
        pass

    def getItems():
        """Returns all items.
        """
        pass

    def hasItems():
        """Returns True if there is at least one item.
        """
        pass