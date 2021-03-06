# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionZenoss/tests/testSiteSetup.py
# Compiled at: 2011-01-11 16:22:56
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
ztc.installProduct('Five')
ztc.installProduct('BastionZenoss')
ptc.setupPloneSite(products=['BastionZenoss'])

class TestSetup(ptc.PloneTestCase):
    """
    Testing with Plone install and Plone skins ...
    """
    __module__ = __name__

    def testZentinel(self):
        self.failUnless('zport' in self.app.objectIds())

    def testPlone(self):
        self.failUnless('plone' in self.app.objectIds())
        plone = self.app.plone
        self.failUnless('zentinel' in plone.objectIds())
        self.failUnless('zenreports' in plone.objectIds())


if __name__ == '__main__':
    framework()
else:

    def test_suite():
        from unittest import TestSuite, makeSuite
        suite = TestSuite()
        suite.addTest(makeSuite(TestSetup))
        return suite