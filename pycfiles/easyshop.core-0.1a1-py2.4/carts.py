# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/interfaces/carts.py
# Compiled at: 2008-06-20 09:35:25
from zope.interface import Interface
from zope.interface import Attribute

class ICart(Interface):
    """A cart of a shop. Can hold serveral cart items.
    """
    __module__ = __name__
    id = Attribute('The unique id of the card. Either the member id or the session id')


class ICartsContainer(Interface):
    """A container which hold carts.
    """
    __module__ = __name__


class ICartManagement(Interface):
    """Provides methods to manage cart content objects
    """
    __module__ = __name__

    def createCart():
        """Creates a cart for the current user.
        """
        pass

    def deleteCart(id):
        """Deletes a cart
        """
        pass

    def getCart():
        """Returns the cart of actual session / authenticated member. Returns
        None if there isn't one.
        """
        pass

    def getCarts(sorted_on='date', sort_order='descending'):
        """Returns carts depending of given paramenters.
        """
        pass

    def getCartById(id):
        """Returns a cart by given id.
        """
        pass

    def hasCart(id):
        """Returns True if the current user has a cart.
        """
        pass


class ICartsContainer(Interface):
    """A marker interface for carts folder content objects.
    """
    __module__ = __name__


class ICartItem(Interface):
    """A cart item holds a selected product and its amount an properties.
    """
    __module__ = __name__
    amount = Attribute('The selected amount of the product')
    product = Attribute('The selected product.')
    properties = Attribute('The selected attributes of the product')