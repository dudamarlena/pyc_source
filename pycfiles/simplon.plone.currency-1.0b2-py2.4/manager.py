# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/simplon/plone/currency/manager.py
# Compiled at: 2007-09-08 18:44:19
from Persistence import Persistent
from zope.interface import implements
from simplon.plone.currency.interfaces import ICurrencyManager
from simplon.plone.currency.currency import CurrencyStorage
from simplon.plone.currency.currency import Currency

class CurrencyManager(Persistent):
    __module__ = __name__
    implements(ICurrencyManager)

    def __init__(self):
        self.currencies = CurrencyStorage()
        self.currencies.addItem(Currency(code='EUR', rate=1.0))
        self.currency = 'EUR'

    def SwitchCurrency(self, code):
        factor = self.currencies[code].rate
        for cur in self.currencies.values():
            cur.rate /= factor

        self.currency = code

    def Convert(from_currency, to_currency, amount):
        return amount * self.currencies[to_curency].rate / self.currencies[from_currency].rate