# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/shop/adapters/currency_management.py
# Compiled at: 2008-09-03 11:15:25
from zope.interface import implements
from zope.component import adapts
from zope.interface import Interface
from easyshop.core.config import CURRENCIES
from easyshop.core.interfaces import ICurrencyManagement
from easyshop.core.interfaces import IShopManagement

class CurrencyManagement:
    """Provides ICurrencyManagement for serveral content objects.
    """
    __module__ = __name__
    implements(ICurrencyManagement)
    adapts(Interface)

    def __init__(self, context):
        """
        """
        self.shop = IShopManagement(context).getShop()

    def getLongName(self):
        """
        """
        currency = self.shop.getCurrency()
        return CURRENCIES[currency]['long']

    def getShortName(self):
        """
        """
        currency = self.shop.getCurrency()
        return CURRENCIES[currency]['short']

    def getSymbol(self):
        """
        """
        currency = self.shop.getCurrency()
        return CURRENCIES[currency]['symbol']

    def priceToString(self, price, symbol='symbol', position='before', prefix=None, suffix='*'):
        """
        """
        price = '%.2f' % price
        price = price.replace('.', ',')
        if symbol == 'short':
            currency = self.getShortName()
        elif symbol == 'long':
            currency = self.getLongName()
        else:
            currency = self.getSymbol()
        if prefix is not None:
            price = '%s%s' % (prefix, price)
        if suffix is not None:
            price = '%s%s' % (price, suffix)
        if position == 'before':
            price = '%s %s' % (currency, price)
        else:
            price = '%s %s' % (price, currency)
        return price