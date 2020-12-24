# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/carts/adapters/taxes.py
# Compiled at: 2008-09-03 11:14:22
from zope.interface import implements
from zope.component import adapts
from easyshop.core.interfaces import ICart
from easyshop.core.interfaces import ICartItem
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IPaymentPriceManagement
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import IShippingPriceManagement
from easyshop.core.interfaces import IShopManagement
from easyshop.core.interfaces import ITaxes

class CartTaxes:
    """Adapter which provides ITaxes for cart content objects.
    """
    __module__ = __name__
    implements(ITaxes)
    adapts(ICart)

    def __init__(self, context):
        """
        """
        self.context = context

    def getTaxRate(self):
        """
        """
        raise ValueError

    def getTaxRateForCustomer(self):
        """
        """
        raise ValueError

    def getTax(self):
        """
        """
        im = IItemManagement(self.context)
        if im.hasItems() == False:
            return 0.0
        tax = 0.0
        for cart_item in im.getItems():
            taxes = ITaxes(cart_item)
            tax += taxes.getTax()

        shop = IShopManagement(self.context).getShop()
        tax += IShippingPriceManagement(shop).getTax()
        tax += IPaymentPriceManagement(shop).getTax()
        return tax

    def getTaxForCustomer(self):
        """
        """
        im = IItemManagement(self.context)
        if im.hasItems() == False:
            return 0.0
        tax = 0.0
        for cart_item in im.getItems():
            taxes = ITaxes(cart_item)
            tax += taxes.getTaxForCustomer()

        shop = IShopManagement(self.context).getShop()
        tax += IShippingPriceManagement(shop).getTaxForCustomer()
        tax += IPaymentPriceManagement(shop).getTaxForCustomer()
        return tax


class CartItemTaxes:
    """Adapter which provides ITaxes for cart item content objects.
    """
    __module__ = __name__
    implements(ITaxes)
    adapts(ICartItem)

    def __init__(self, context):
        """
        """
        self.context = context
        self.taxes = ITaxes(self.context.getProduct())

    def getTax(self):
        """Returns absolute tax.
        """
        price = IPrices(self.context).getPriceGross(with_discount=True)
        tax_rate = self.taxes.getTaxRate()
        tax = tax_rate / (tax_rate + 100) * price
        return tax

    def getTaxForCustomer(self):
        """Returns absolute tax for customer.
        """
        price = IPrices(self.context).getPriceGross(with_discount=True)
        tax_rate = self.taxes.getTaxRateForCustomer()
        tax = tax_rate / (tax_rate + 100) * price
        return tax

    def getTaxRate(self):
        """Returns tax rate
        """
        tax_rate = self.taxes.getTaxRate()
        return tax_rate

    def getTaxRateForCustomer(self):
        """Returns tax rate for a customer.
        """
        tax = self.taxes.getTaxRateForCustomer() * self.context.getAmount()
        return tax