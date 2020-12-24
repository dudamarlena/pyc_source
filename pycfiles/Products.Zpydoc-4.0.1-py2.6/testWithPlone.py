# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/Zpydoc/tests/testWithPlone.py
# Compiled at: 2011-09-28 02:31:46
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
import zLOG
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.Zpydoc.config import TOOLNAME
ztc.installProduct('Zpydoc')
ptc.setupPloneSite(products=['Zpydoc'])

class TestZpydoc(ptc.PloneTestCase):
    """
    Testing with Plone install and Plone skins ...
    """

    def afterSetUp(self):
        ptc.PloneTestCase.afterSetUp(self)
        self.portal.manage_addProduct['Zpydoc'].manage_addZpydoc()
        self.zpydoc = getattr(self.portal, TOOLNAME)
        self.portal.portal_quickinstaller.installProduct('Zpydoc')

    def testUnsafeZpyDocumentable(self):
        self.zpydoc.manage_addProduct['Zpydoc'].manage_addZpyDocumentable(os.path.dirname(os.path.dirname(__file__)), 'Zope')
        getattr(self.zpydoc, '0')._file_permissions['Zpydoc'] = {'anonymous': 1}
        self.failUnless(self.zpydoc.zpydoc_view())

    def testTest(self):
        self.failUnless(TOOLNAME in self.portal.objectIds())
        self.failUnless(self.zpydoc.zpydoc_view())


if __name__ == '__main__':
    framework()
else:

    def test_suite():
        from unittest import TestSuite, makeSuite
        suite = TestSuite()
        suite.addTest(makeSuite(TestZpydoc))
        return suite