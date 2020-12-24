# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/simplon/plone/currency/tests/testCurrency.py
# Compiled at: 2007-09-08 18:44:19
from simplon.plone.currency.currency import Currency
from simplon.plone.currency.interfaces import ICurrency
from zope.interface.verify import verifyObject
import unittest

class CurrencyTests(unittest.TestCase):
    __module__ = __name__

    def testInterface(self):
        euro = Currency(code='EUR', rate='1.0')
        verifyObject(ICurrency, euro)

    def testConstruction(self):
        euro = Currency(code='EUR', rate=1.0)
        self.assertEqual(euro.code, 'EUR')
        self.assertEqual(euro.rate, 1.0)
        usd = Currency(code='USD', rate=0.72)
        self.assertEqual(usd.code, 'USD')
        self.assertEqual(usd.rate, 0.72)

    def testCurrencySymbolKnowledge(self):
        self.assertEqual(Currency('EUR').symbol, '€')
        self.assertEqual(Currency('USD').symbol, '$')
        self.assertEqual(Currency('NOK').symbol, 'NOK')

    def testCurrencySymbolKnowledge(self):
        self.assertEqual(Currency('EUR').description, 'Euro')
        self.assertEqual(Currency('USD').description, 'US Dollar')
        self.assertEqual(Currency('NOK').description, 'Norwegian Krone')


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(CurrencyTests))
    return suite