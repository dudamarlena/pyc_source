# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/carts/adapters/discounts_calculation.py
# Compiled at: 2008-09-03 11:14:22
from zope.interface import implements
from zope.component import adapts
from easyshop.core.interfaces import ICart
from easyshop.core.interfaces import ICartItem
from easyshop.core.interfaces import IDiscountsCalculation
from easyshop.core.interfaces import IDiscountsManagement
from easyshop.core.interfaces import IShopManagement
from easyshop.core.interfaces import IValidity

class CartDiscountsCalculation:
    """An adapter which provides IDiscountsCalculation for cart content objects.
    """
    __module__ = __name__
    implements(IDiscountsCalculation)
    adapts(ICart)

    def __init__(self, context):
        """
        """
        self.context = context

    def getDiscount(self):
        """Returns calculated discounts.
        """
        return self.getDiscountsInformation()['discounts']


class CartItemDiscountsCalculation:
    """An adapter which provides IDiscountsCalculation for cart item content
    objects.
    """
    __module__ = __name__
    implements(IDiscountsCalculation)
    adapts(ICartItem)

    def __init__(self, context):
        """
        """
        self.context = context

    def getDiscount(self):
        """Returns the first valid discount or None.
        """
        shop = IShopManagement(self.context.getProduct()).getShop()
        for discount in IDiscountsManagement(shop).getDiscounts():
            if IValidity(discount).isValid(self.context) == True:
                return discount

        return