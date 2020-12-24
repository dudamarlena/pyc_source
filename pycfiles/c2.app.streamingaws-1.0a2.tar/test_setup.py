# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/c2/app/shorturl/tests/test_setup.py
# Compiled at: 2010-08-19 05:10:30
__doc__ = '\ntest_setup.py\n\nCreated by Manabu Terada on 2010-08-03.\nCopyright (c) 2010 CMScom. All rights reserved.\n'
from Products.CMFCore.utils import getToolByName
import c2.app.shorturl, base

class TestInstall(base.BaseTestCase):
    """ Install basic test """

    def afterSetUp(self):
        pass

    def testQuickInstall(self):
        qi = self.portal.portal_quickinstaller
        self.failUnless('c2.app.shorturl' in (p['id'] for p in qi.listInstallableProducts()))
        qi.installProduct('c2.app.shorturl')
        self.failUnless(qi.isProductInstalled('c2.app.shorturl'))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestInstall))
    return suite