# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/c2/app/shorturl/tests/test_setup.py
# Compiled at: 2010-08-19 05:10:30
"""
test_setup.py

Created by Manabu Terada on 2010-08-03.
Copyright (c) 2010 CMScom. All rights reserved.
"""
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