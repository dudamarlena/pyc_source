# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/interfaces/orders.py
# Compiled at: 2008-06-20 09:35:25
from zope.interface import Interface
from zope.interface import Attribute

class IOrder(Interface):
    """An marker interface for order content objects.
    """
    __module__ = __name__


class IOrderManagement(Interface):
    """Provides methods to manage order content objects.
    """
    __module__ = __name__

    def addOrder(customer=None, cart=None):
        """Adds a new order on base of the current customer and current cart.
        """
        pass

    def deleteOrder(id):
        """Deletes order with given id.
        """
        pass

    def getOrderByUID(uid):
        """Returns order by given uid.        
        """
        pass

    def getOrders(filter=None):
        """Returns orders filtered by given filter.
        """
        pass

    def getOrdersForAuthenticatedCustomer():
        """Returns all orders for the current customer
        """
        pass

    def getOrdersForCustomer(customer_id):
        """Returns orders for customer with given id.
        """
        pass


class IOrderItem(Interface):
    """Marker interface to mark order item content objects.
    """
    __module__ = __name__


class IOrdersContainer(Interface):
    """An marker interface for containers which hold orders.
    """
    __module__ = __name__


class IOrderSubmitted(Interface):
    """An event fired when an order has been submitted.
    """
    __module__ = __name__
    context = Attribute('The order that has been submitted')


class IOrderPayed(Interface):
    """An event fired when an order has been payed.
    """
    __module__ = __name__
    context = Attribute('The order that has been payed')


class IOrderSent(Interface):
    """An event fired when an order has been sent
    """
    __module__ = __name__
    context = Attribute('The order that has been sent')


class IOrderClosed(Interface):
    """An event fired when an order has been closed
    """
    __module__ = __name__
    context = Attribute('The order that has been closed')