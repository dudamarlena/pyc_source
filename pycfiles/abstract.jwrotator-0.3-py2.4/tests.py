# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/abstract/jwrotator/tests.py
# Compiled at: 2008-07-09 06:34:27
import unittest
from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Products.Five.testbrowser import Browser
from Products.CMFCore.utils import getToolByName
ptc.setupPloneSite(products=['abstract.jwrotator'])
import abstract.jwrotator

class TestCase(ptc.PloneTestCase):
    __module__ = __name__

    class layer(PloneSite):
        __module__ = __name__

        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            zcml.load_config('configure.zcml', abstract.jwrotator)
            fiveconfigure.debug_mode = False

        @classmethod
        def tearDown(cls):
            pass

    def testProperInstall(self):
        """Test if product install properly"""
        qi_tool = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(qi_tool.isProductInstalled('abstract.jwrotator'))

    def testViewMethods(self):
        """test if jwrotator_vew is installed properly"""
        pt_tool = getToolByName(self.portal, 'portal_types')
        view_types = ['Folder', 'Topic', 'Large Plone Folder']
        for view_type in view_types:
            folder_view_methods = list(pt_tool[view_type].view_methods)
            self.failUnless('jwrotator_view' in folder_view_methods)

    def testEmbeddedSWF(self):
        """test if SWF is embedded in the view"""
        self.setRoles(('Manager', ))
        self.portal.invokeFactory('Folder', 'folder_image')
        folder = getattr(self.portal, 'folder_image')
        folder.setLayout('jwrotator_view')


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCase))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')