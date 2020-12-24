# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/discounts/adapters/prices.py
# Compiled at: 2008-09-03 11:14:47
from zope.interface import implements
from zope.component import adapts
from easyshop.core.interfaces import ICartItem
from easyshop.core.interfaces import IDiscount
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import IShopManagement
from easyshop.core.interfaces import ITaxes

class DiscountPrices:
    """Multia adapter which provides IPrices for discount content objects and 
    product.
    """
    __module__ = __name__
    implements(IPrices)
    adapts(IDiscount, ICartItem)

    def __init__(self, discount, cart_item):
        """
        """
        self.discount = discount
        self.cart_item = cart_item
        self.product = cart_item.getProduct()
        self.taxes = ITaxes(self.product)
        self.shop = IShopManagement(self.product).getShop()

    def getPriceForCustomer(self):
        """
        """
        if self.discount.getType() == 'percentage':
            price = IPrices(self.cart_item).getPriceForCustomer()
            return price * (self.discount.getValue() / 100)
        else:
            tax_rate_for_customer = self.taxes.getTaxRateForCustomer()
            price_net = self.getPriceNet()
            return price_net * ((tax_rate_for_customer + 100) / 100)

    def getPriceGross(self):
        """
        """
        if self.discount.getType() == 'percentage':
            price = IPrices(self.cart_item).getPriceGross()
            return price * (self.discount.getValue() / 100)
        else:
            tax_rate = self.taxes.getTaxRate()
            price = self._calcTotalPrice()
            if self.shop.getGrossPrices() == True:
                return price
            else:
                return price * ((tax_rate + 100) / 100)

    def getPriceNet(self):
        """
        """
        if self.discount.getType() == 'percentage':
            price = IPrices(self.cart_item).getPriceNet()
            return price * (self.discount.getValue() / 100)
        else:
            tax_rate = self.taxes.getTaxRate()
            price = self._calcTotalPrice()
            if self.shop.getGrossPrices() == True:
                return price * (100 / (tax_rate + 100))
            else:
                return price

    def _calcTotalPrice(self):
        """
        """
        if self.discount.getBase() == 'cart_item':
            return self.discount.getValue()
        else:
            return self.discount.getValue() * self.cart_item.getAmount()