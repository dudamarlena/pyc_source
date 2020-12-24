# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/interfaces/stocks.py
# Compiled at: 2008-06-20 09:35:25
from zope.interface import Attribute
from zope.interface import Interface

class IStockInformation(Interface):
    """Holds availability of products and time period of shipping.
    """
    __module__ = __name__


class IStockInformationContainer(Interface):
    """A simple container to holds stock information.
    """
    __module__ = __name__


class IStockManagement(Interface):
    """Provides methods to manage stock information.
    """
    __module__ = __name__

    def getStockInformations():
        """Returns existing stock information.
        """
        pass

    def getStockInformationFor(product):
        """Returns first valid stock information for given product.
        """
        pass

    def removeCart(cart):
        """Removes product which are within given cart from stock.
        """
        pass


class IAvailablility(Interface):
    """Provides calculation of availability of a product.
    """
    __module__ = __name__

    def isAvailable():
        """Returns True if the product is available.
        """
        pass


class IStockAmountIsZeroEvent(Interface):
    """An event which is sent when the stock amount of a product is zero or 
    less.
    """
    __module__ = __name__
    product = Attribute('The product for which the stock amount is zero.')