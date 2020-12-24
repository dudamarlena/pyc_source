# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\Products\ATGoogleMaps\tests\test_setup.py
# Compiled at: 2010-06-03 09:07:24
__doc__ = '\ntest_setup.py\n\nCreated by Manabu Terada on 2009-12-16.\nCopyright (c) 2009 CMScom. All rights reserved.\n'
from Products.CMFCore.utils import getToolByName
import Products.ATGoogleMaps, base

class TestInstall(base.TestCase):
    """ Install basic test """

    def afterSetUp(self):
        pass

    def testQuickInstall(self):
        qi = self.portal.portal_quickinstaller
        print ('\n').join(p['id'] for p in qi.listInstallableProducts())
        self.failUnless(1, len([ p['title'] for p in qi.listInstallableProducts() if p['title'] == 'ATGoogleMaps'
                               ]))
        self.failUnless('ATGoogleMaps' in (p['id'] for p in qi.listInstallableProducts()))
        qi.installProduct('ATGoogleMaps')
        self.failUnless(qi.isProductInstalled('ATGoogleMaps'))
        self.failUnless('ATGoogleMaps' not in ('').join(p['id'] for p in qi.listInstallableProducts()))


class TestSkinInstall(base.TestCase):
    """  """

    def afterSetUp(self):
        qi = self.portal.portal_quickinstaller
        qi.installProduct('ATGoogleMaps')

    def testSkinLayersInstalled(self):
        self.skins = self.portal.portal_skins
        self.failUnless('ATGoogleMaps' in self.skins.objectIds())
        self.assertEqual(len(self.skins.ATGoogleMaps.objectIds()), 1)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestInstall))
    suite.addTest(makeSuite(TestSkinInstall))
    return suite