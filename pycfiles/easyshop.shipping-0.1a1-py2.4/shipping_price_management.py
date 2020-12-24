# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/shipping/adapters/shipping_price_management.py
# Compiled at: 2008-09-03 11:15:18
from zope.interface import implements
from zope.component import adapts
from Products.CMFCore.utils import getToolByName
from easyshop.core.interfaces import ITaxes
from easyshop.core.interfaces import IShippingPriceManagement
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IValidity
from easyshop.core.interfaces import IShop
from easyshop.catalog.content.product import Product
from easyshop.core.interfaces import IShopManagement

class ShippingPriceManagement(object):
    """An adapter which provides IShippingPriceManagement for shop content objects.
    """
    __module__ = __name__
    implements(IShippingPriceManagement)
    adapts(IShop)

    def __init__(self, context):
        """
        """
        self.context = context
        self.prices = self.context.shippingprices
        self.methods = self.context.shippingmethods

    def getShippingPrice(self, id):
        """
        """
        try:
            return self.prices[id]
        except KeyError:
            return

        return

    def getShippingPrices(self):
        """
        """
        return self.prices.objectValues()

    def getPriceForCustomer(self):
        """
        """
        cart_manager = ICartManagement(self.context)
        cart = cart_manager.getCart()
        if cart is None:
            return 0
        cart_item_manager = IItemManagement(cart)
        if cart_item_manager.hasItems() == False:
            return 0
        return self.getPriceNet() + self.getTaxForCustomer()

    def getPriceGross(self):
        """
        """
        for price in self.getShippingPrices():
            if IValidity(price).isValid() == True:
                return price.getPrice()

        return 0

    def getPriceNet(self):
        """
        """
        return self.getPriceGross() - self.getTax()

    def getTaxRate(self):
        """
        """
        temp_shipping_product = self._createTemporaryShippingProduct()
        return ITaxes(temp_shipping_product).getTaxRate()

    def getTaxRateForCustomer(self):
        """
        """
        temp_shipping_product = self._createTemporaryShippingProduct()
        return ITaxes(temp_shipping_product).getTaxRateForCustomer()

    def getTax(self):
        """
        """
        temp_shipping_product = self._createTemporaryShippingProduct()
        return ITaxes(temp_shipping_product).getTax()

    def getTaxForCustomer(self):
        """
        """
        cart_manager = ICartManagement(self.context)
        cart = cart_manager.getCart()
        if cart is None:
            return 0
        cart_item_manager = IItemManagement(cart)
        if cart_item_manager.hasItems() == False:
            return 0
        temp_shipping_product = self._createTemporaryShippingProduct()
        return ITaxes(temp_shipping_product).getTaxForCustomer()

    def _createTemporaryShippingProduct(self):
        """
        """
        temp_shipping_product = Product('shipping')
        temp_shipping_product.setPrice(self.getPriceGross())
        temp_shipping_product.context = self.context
        return temp_shipping_product