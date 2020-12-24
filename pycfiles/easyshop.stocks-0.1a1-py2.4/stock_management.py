# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/stocks/adapters/stock_management.py
# Compiled at: 2008-09-03 11:15:30
from zope.component import adapts
from zope.event import notify
from zope.interface import implements
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IShop
from easyshop.core.interfaces import IStockManagement
from easyshop.core.interfaces import IValidity
from easyshop.stocks.events import StockAmountIsZeroEvent

class StockManagement:
    """Adapter which provides IStockManagement for shop content objects.
    """
    __module__ = __name__
    implements(IStockManagement)
    adapts(IShop)

    def __init__(self, context):
        """
        """
        self.context = context
        self.stock_information = context['stock-information']

    def getStockInformationFor(self, product):
        """
        """
        for information in self.stock_information.objectValues():
            if IValidity(information).isValid(product) == True:
                return information

        return

    def getStockInformations(self):
        """
        """
        return self.stock_information.objectValues()

    def removeCart(self, cart):
        """
        """
        for cart_item in IItemManagement(cart).getItems():
            product = cart_item.getProduct()
            if product.getUnlimitedAmount() == False:
                amount = cart_item.getAmount()
                new_amount = product.getStockAmount() - amount
                product.setStockAmount(new_amount)
                if new_amount <= 0:
                    notify(StockAmountIsZeroEvent(product))