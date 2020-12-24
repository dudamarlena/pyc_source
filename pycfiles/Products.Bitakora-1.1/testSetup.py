# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/Products/BigramSplitter/tests/testSetup.py
# Compiled at: 2010-12-06 08:32:12
from Products.CMFCore.utils import getToolByName
from Products import BigramSplitter
from Products.BigramSplitter.config import *
import base

class TestInstall(base.BigramSplitterTestCase):
    """ Install basic test """
    __module__ = __name__

    def afterSetUp(self):
        pass

    def testQuickInstall(self):
        qi = self.portal.portal_quickinstaller
        self.failUnless('BigramSplitter' in (p['id'] for p in qi.listInstallableProducts()))
        qi.installProduct('BigramSplitter')
        self.failUnless(qi.isProductInstalled('BigramSplitter'))


class TestSkinInstall(base.BigramSplitterTestCase):
    """  """
    __module__ = __name__

    def afterSetUp(self):
        qi = self.portal.portal_quickinstaller
        qi.installProduct('BigramSplitter')

    def testSkinLayersInstalled(self):
        self.skins = self.portal.portal_skins
        self.failUnless('BigramSplitter' in self.skins.objectIds())
        self.assertEqual(len(self.skins.BigramSplitter.objectIds()), 1)


class TestReplaceCatalog(base.BigramSplitterTestCase):
    """ Replace the catalog """
    __module__ = __name__

    def afterSetUp(self):
        qi = self.portal.portal_quickinstaller
        qi.installProduct('BigramSplitter')

    def testWordSplitter(self):
        from Products.ZCTextIndex.PipelineFactory import element_factory
        group = 'Word Splitter'
        names = element_factory.getFactoryNames(group)
        self.failUnless('Bigram Splitter' in names)
        group = 'Case Normalizer'
        names = element_factory.getFactoryNames(group)
        self.failUnless('Bigram Case Normalizer' in names)

    def testCatalogTitle(self):
        cat = getToolByName(self.portal, 'portal_catalog')
        self.failUnless('Title' in cat.indexes())
        self.failUnless('bigram_lexicon' in [ ix.getLexicon().id for ix in cat.index_objects() if ix.id == 'Title' ])

    def testCatalogDescription(self):
        cat = getToolByName(self.portal, 'portal_catalog')
        self.failUnless('Description' in cat.indexes())
        self.failUnless('bigram_lexicon' in [ ix.getLexicon().id for ix in cat.index_objects() if ix.id == 'Description' ])

    def testSearchableText(self):
        cat = getToolByName(self.portal, 'portal_catalog')
        self.failUnless('SearchableText' in cat.indexes())
        self.failUnless('bigram_lexicon' in [ ix.getLexicon().id for ix in cat.index_objects() if ix.id == 'SearchableText' ])


class TestUninstall(base.BigramSplitterTestCase):
    """ Uninstall test """
    __module__ = __name__

    def afterSetUp(self):
        pass

    def testQuickUninstall(self):
        qi = self.portal.portal_quickinstaller
        qi.installProduct('BigramSplitter')
        self.failUnless(qi.isProductInstalled('BigramSplitter'))
        qi.uninstallProducts(['BigramSplitter'])
        self.failUnless('BigramSplitter' in (p['id'] for p in qi.listInstallableProducts()))

    def testWordSplitter(self):
        cat = getToolByName(self.portal, 'portal_catalog')
        qi = self.portal.portal_quickinstaller
        qi.installProduct('BigramSplitter')
        names = cat.objectIds()
        self.failUnless('bigram_lexicon' in names)

    def testCatalogTitle(self):
        cat = getToolByName(self.portal, 'portal_catalog')
        qi = self.portal.portal_quickinstaller
        qi.installProduct('BigramSplitter')
        self.failUnless('bigram_lexicon' in [ ix.getLexicon().id for ix in cat.index_objects() if ix.id == 'Title' ])

    def testCatalogDescription(self):
        cat = getToolByName(self.portal, 'portal_catalog')
        qi = self.portal.portal_quickinstaller
        qi.installProduct('BigramSplitter')
        self.failUnless('bigram_lexicon' in [ ix.getLexicon().id for ix in cat.index_objects() if ix.id == 'Description' ])

    def testSearchableText(self):
        cat = getToolByName(self.portal, 'portal_catalog')
        qi = self.portal.portal_quickinstaller
        qi.installProduct('BigramSplitter')
        self.failUnless('bigram_lexicon' in [ ix.getLexicon().id for ix in cat.index_objects() if ix.id == 'SearchableText' ])


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestInstall))
    suite.addTest(makeSuite(TestSkinInstall))
    suite.addTest(makeSuite(TestUninstall))
    suite.addTest(makeSuite(TestReplaceCatalog))
    return suite