# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/c2/search/customdescription/tests/test_setup.py
# Compiled at: 2009-12-04 01:50:08
__doc__ = '\ntest_setup.py\n\nCreated by Manabu Terada on 2009-11-11.\nCopyright (c) 2009 CMScom. All rights reserved.\n'
from Products.CMFCore.utils import getToolByName
import c2.search.customdescription, base

class TestInstall(base.ProductTestCase):
    """ Install basic test """
    __module__ = __name__

    def afterSetUp(self):
        pass

    def testQuickInstall(self):
        qi = self.portal.portal_quickinstaller
        self.failUnless('c2.search.customdescription' in (p['id'] for p in qi.listInstallableProducts()))
        qi.installProduct('c2.search.customdescription')
        self.failUnless(qi.isProductInstalled('c2.search.customdescription'))


class TestSkinInstall(base.ProductTestCase):
    """  """
    __module__ = __name__

    def afterSetUp(self):
        qi = self.portal.portal_quickinstaller
        qi.installProduct('c2.search.customdescription')

    def testSkinLayersInstalled(self):
        self.skins = self.portal.portal_skins
        self.failUnless('c2customdescription' in self.skins.objectIds())
        self.assertEqual(len(self.skins.c2customdescription.objectIds()), 1)


class TestAddingCatalog(base.ProductTestCase):
    """ adding the catalog metadata"""
    __module__ = __name__

    def afterSetUp(self):
        qi = self.portal.portal_quickinstaller
        qi.installProduct('c2.search.customdescription')

    def testMetadata(self):
        cat = getToolByName(self.portal, 'portal_catalog')
        self.failUnless('SearchableText' in cat.schema())


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestInstall))
    suite.addTest(makeSuite(TestSkinInstall))
    suite.addTest(makeSuite(TestAddingCatalog))
    return suite