# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/c2/patch/effectivedateforlisting/tests/test_setup.py
# Compiled at: 2010-01-30 03:43:31
__doc__ = '\ntest_setup.py\n\nCreated by Manabu Terada on 2010-01-29.\nCopyright (c) 2010 CMScom. All rights reserved.\n'
from Products.CMFCore.utils import getToolByName
import c2.patch.effectivedateforlisting, base

class TestInstall(base.ProductTestCase):
    """ Install basic test """
    __module__ = __name__

    def afterSetUp(self):
        pass

    def testQuickInstall(self):
        qi = self.portal.portal_quickinstaller
        self.failUnless('c2.patch.effectivedateforlisting' in (p['id'] for p in qi.listInstallableProducts()))
        qi.installProduct('c2.patch.effectivedateforlisting')
        self.failUnless(qi.isProductInstalled('c2.patch.effectivedateforlisting'))


class TestSkinInstall(base.ProductTestCase):
    """  """
    __module__ = __name__

    def afterSetUp(self):
        qi = self.portal.portal_quickinstaller
        qi.installProduct('c2.patch.effectivedateforlisting')

    def testSkinLayersInstalled(self):
        self.skins = self.portal.portal_skins
        self.failUnless('c2effectivedateforlisting' in self.skins.objectIds())
        self.assertEqual(len(self.skins.c2effectivedateforlisting.objectIds()), 1)

    def testSkinLayersOrderd(self):
        self.skins = self.portal.portal_skins
        layer_orderd = self.skins.getSkinPaths()[0][1].split(',')
        self.assertEqual(layer_orderd[0], 'custom')
        self.assertEqual(layer_orderd[1], 'c2effectivedateforlisting')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestInstall))
    suite.addTest(makeSuite(TestSkinInstall))
    return suite