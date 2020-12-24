# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/interfaces/shipping.py
# Compiled at: 2008-06-20 09:35:25
from zope.interface import Interface

class IShippingMethodManagement(Interface):
    """
    """
    __module__ = __name__

    def getSelectedShippingMethod():
        """Returns the selected shipping method of the current authenticated 
        customer.
        """
        pass

    def getShippingMethod(id):
        """Returns shipping method by given id.
        """
        pass

    def getShippingMethods():
        """Returns all shipping methods.
        """
        pass


class IShippingPriceManagement(Interface):
    """Provides all methods to manage the shipping prices. This includes also 
    calculation of prices and taxes (maybe this will separated later to 
    different interfaces, e.g.: IShippingPriceManagement, IShippingPrices, 
    IShippingTaxes).
    """
    __module__ = __name__

    def getPriceNet():
        """Returns the net price of shipping.
        """
        pass

    def getPriceGross():
        """Returns the gross price of shipping. Returns the first valid        
        (All criteria are True) shipping price.
        """
        pass

    def getPriceForCustomer():
        """Returns the gross price of shipping for actual customer
        """
        pass

    def getShippingPrice(id):
        """Returns shipping price by given id
        """
        pass

    def getShippingPrices():
        """Returns all shipping prices
        """
        pass

    def getTaxRate():
        """Returns tax rate for shipping by means of tax manager
        """
        pass

    def getTaxRateForCustomer():
        """Returns tax for shipping for actual customer by means of tax
           manager
        """
        pass

    def getTax():
        """Returns absolute tax for shipping by means of tax manager
        """
        pass

    def getTaxForCustomer():
        """Returns absolute tax for shipping for actual customer by means of
           tax manager
        """
        pass


class IShippingPrice(Interface):
    """A price for shipping.
    """
    __module__ = __name__


class IShippingMethod(Interface):
    """A shipping method.
    """
    __module__ = __name__


class IShippingPricesContainer(Interface):
    """A container to hold shipping prices
    """
    __module__ = __name__


class IShippingMethodsContainer(Interface):
    """A container to hold shipping methods
    """
    __module__ = __name__