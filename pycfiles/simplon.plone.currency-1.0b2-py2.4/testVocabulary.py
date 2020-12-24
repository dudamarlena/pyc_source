# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/simplon/plone/currency/tests/testVocabulary.py
# Compiled at: 2007-09-08 18:44:19
from simplon.plone.currency.vocabulary import CurrencyVocabularyFactory
from simplon.plone.currency.vocabulary import SiteCurrencyVocabularyFactory
from simplon.plone.currency.interfaces import ICurrencyManager
from simplon.plone.currency.manager import CurrencyManager
from simplon.plone.currency.currency import Currency
from zope.schema.interfaces import IVocabularyFactory
from zope.component.globalregistry import base
from zope.interface.verify import verifyObject
import unittest

class CurrencyVocabularyTests(unittest.TestCase):
    __module__ = __name__

    def setUp(self):
        self.vocabulary = CurrencyVocabularyFactory

    def XXXtestInterface(self):
        verifyObject(IVocabularyFactory, self.vocabulary)

    def testContains(self):
        self.failUnless('EUR' in self.vocabulary(None))
        self.failUnless('NOK' in self.vocabulary(None))
        self.failIf('XXX' in self.vocabulary(None))
        return


class SiteCurrencyVocabularyTests(unittest.TestCase):
    __module__ = __name__

    def setUp(self):
        self.vocabulary = SiteCurrencyVocabularyFactory
        self.manager = CurrencyManager()
        base.registerUtility(self.manager, ICurrencyManager)

    def tearDown(self):
        base.unregisterUtility(self.manager, ICurrencyManager)

    def testInitialVocabulary(self):
        self.assertEqual(len(self.vocabulary(None)), 1)
        self.assertEqual([ t.value for t in self.vocabulary(None) ], ['EUR'])
        return

    def testNewCurrencies(self):
        self.manager.currencies.addItem(Currency(code='NOK'))
        self.assertEqual(len(self.vocabulary(None)), 2)
        self.assertEqual(set([ t.value for t in self.vocabulary(None) ]), set(['EUR', 'NOK']))
        return

    def testRemovingCurrencies(self):
        self.manager.currencies.addItem(Currency(code='NOK'))
        del self.manager.currencies['EUR']
        self.assertEqual(len(self.vocabulary(None)), 1)
        self.assertEqual([ t.value for t in self.vocabulary(None) ], ['NOK'])
        return


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(CurrencyVocabularyTests))
    suite.addTest(unittest.makeSuite(SiteCurrencyVocabularyTests))
    return suite