# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/Products/BigramSplitter/tests/testJapanese.py
# Compiled at: 2010-01-29 04:56:14
from Products.CMFCore.utils import getToolByName
from Products import BigramSplitter
from Products.BigramSplitter.config import *
import base

class TestSearchingJapanese(base.BigramSplitterTestCase):
    """ Install Japanese test """
    __module__ = __name__

    def afterSetUp(self):
        qi = self.portal.portal_quickinstaller
        qi.installProduct('BigramSplitter')
        self.setRoles(('Manager', ))
        self.portal.invokeFactory('Document', 'doc1')
        self.doc1 = getattr(self.portal, 'doc1')
        self.doc1.setTitle('Ploneは素晴らしい。')
        self.doc1.setText('このページは予想している通り、テストです。 Pages Testing.')
        self.doc1.reindexObject()

    def testSearch(self):
        catalog = getToolByName(self.portal, 'portal_catalog')
        items1 = catalog(SearchableText='予想')
        self.assertEqual(len(items1), 1)
        items12 = catalog(SearchableText='素晴らしい')
        self.assertEqual(len(items12), 1)
        items13 = catalog(SearchableText='Pages')
        self.assertEqual(len(items13), 1)
        items14 = catalog(SearchableText='ページ')
        self.assertEqual(len(items14), 1)
        items15 = catalog(SearchableText='予想*')
        self.assertEqual(len(items15), 1)
        items16 = catalog(SearchableText='予想')
        self.assertEqual(len(items16), 1)
        items17 = catalog(SearchableText='予想\u3000テスト')
        self.assertEqual(len(items17), 1)
        self.portal.manage_delObjects(['doc1'])
        items2 = catalog(SearchableText='予想')
        self.assertEqual(len(items2), 0)


class TestSearchingUnicodeJapanese(base.BigramSplitterTestCase):
    """ Install Unicode Japanese test """
    __module__ = __name__

    def afterSetUp(self):
        qi = self.portal.portal_quickinstaller
        qi.installProduct('BigramSplitter')
        self.setRoles(('Manager', ))
        self.portal.invokeFactory('Document', 'doc1')
        self.doc1 = getattr(self.portal, 'doc1')
        self.doc1.setTitle('Ploneは素晴らしい。')
        self.doc1.setText('このページは予想している通り、テストです。 Pages Testing.')
        self.doc1.reindexObject()

    def testSearch(self):
        catalog = getToolByName(self.portal, 'portal_catalog')
        items1 = catalog(SearchableText='予想')
        self.assertEqual(len(items1), 1)
        items12 = catalog(SearchableText='素晴らしい')
        self.assertEqual(len(items12), 1)
        items13 = catalog(SearchableText='Pages')
        self.assertEqual(len(items13), 1)
        items14 = catalog(SearchableText='ページ')
        self.assertEqual(len(items14), 1)
        items15 = catalog(SearchableText='予想*')
        self.assertEqual(len(items15), 1)
        items16 = catalog(SearchableText='予想')
        self.assertEqual(len(items16), 1)
        items17 = catalog(SearchableText='予想\u3000テスト')
        self.portal.manage_delObjects(['doc1'])
        items2 = catalog(SearchableText='予想')
        self.assertEqual(len(items2), 0)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestSearchingJapanese))
    suite.addTest(makeSuite(TestSearchingUnicodeJapanese))
    return suite