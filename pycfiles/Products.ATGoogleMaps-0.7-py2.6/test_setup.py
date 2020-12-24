# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Products\ATGoogleMaps\tests\test_setup.py
# Compiled at: 2010-06-03 09:07:24
"""
test_setup.py

Created by Manabu Terada on 2009-12-16.
Copyright (c) 2009 CMScom. All rights reserved.
"""
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