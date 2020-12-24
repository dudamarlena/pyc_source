# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Products/pluggablecatalog/tests/testSetup.py
# Compiled at: 2008-07-23 15:36:19
from Products.pluggablecatalog.tests import common
common.setupPloneSite()
from Products.PloneTestCase import PloneTestCase
from Products.pluggablecatalog import tool
from Products.pluggablecatalog.Extensions import install

class Test(PloneTestCase.PloneTestCase):
    __module__ = __name__

    def afterSetUp(self):
        self.loginAsPortalOwner()

    def testCatalogExists(self):
        install.install(self.portal)
        self.failUnless(isinstance(self.portal.portal_catalog.aq_base, tool.CatalogTool))

    def testReinstall(self):
        install.install(self.portal)
        catalog = self.portal.portal_catalog.aq_base
        install.install(self.portal)
        self.failUnless(catalog is self.portal.portal_catalog.aq_base)

    def testQuickInstallable(self):
        qi = self.portal.portal_quickinstaller
        qi.installProducts(('pluggablecatalog', ))
        self.failUnless(isinstance(self.portal.portal_catalog.aq_base, tool.CatalogTool))

    def testReindex(self):
        self.folder.invokeFactory('Document', 'mydocument')
        mydoc = self.folder.mydocument
        mydoc.setTitle('My Document')
        mydoc.reindexObject()
        brains = self.portal.portal_catalog(Title='My Document')
        self.assertEquals(len(brains), 1)
        self.failUnless(brains[0].getObject().aq_base is mydoc.aq_base)
        install.install(self.portal)
        brains = self.portal.portal_catalog(Title='My Document')
        self.assertEquals(len(brains), 1)
        self.failUnless(brains[0].getObject().aq_base is mydoc.aq_base)
        self.assertEquals(brains[0].Title, 'My Document')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(Test))
    return suite