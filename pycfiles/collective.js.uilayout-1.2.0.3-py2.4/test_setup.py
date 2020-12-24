# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/collective/js/uilayout/tests/test_setup.py
# Compiled at: 2009-11-06 07:52:04
"""This is an integration "unit" test. It uses PloneTestCase, but does not
use doctest syntax.

You will find lots of examples of this type of test in CMFPlone/tests, for 
example.
"""
import unittest
from collective.js.uilayout.tests.base import UILayoutTestCase
from Products.CMFCore.utils import getToolByName

class TestSetup(UILayoutTestCase):
    """The name of the class should be meaningful. This may be a class that
    tests the installation of a particular product.
    """
    __module__ = __name__

    def afterSetUp(self):
        """This method is called before each single test. It can be used to
        set up common state. Setup that is specific to a particular test 
        should be done in that test method.
        """
        self.jsregistry = getToolByName(self.portal, 'portal_javascripts')
        self.cssregistry = getToolByName(self.portal, 'portal_css')
        self.quickinstaller = getToolByName(self.portal, 'portal_quickinstaller')

    def beforeTearDown(self):
        """This method is called after each single test. It can be used for
        cleanup, if you need it. Note that the test framework will roll back
        the Zope transaction at the end of each test, so tests are generally
        independent of one another. However, if you are modifying external
        resources (say a database) or globals (such as registering a new
        adapter in the Component Architecture during a test), you may want to
        tear things down here.
        """
        pass

    def test_products_installed(self):
        self.failUnless(self.quickinstaller.isProductInstalled('collective.js.jquery'))
        self.failUnless(self.quickinstaller.isProductInstalled('collective.js.jqueryui'))
        self.failUnless(self.quickinstaller.isProductInstalled('collective.js.uilayout'))

    def test_javascript_installed(self):
        self.failUnless(self.jsregistry.getResource('++resource++jquery.layout.min.js') is not None)
        return

    def test_css_installed(self):
        self.failUnless(self.cssregistry.getResource('++resource++jquery.layout.css') is not None)
        self.failUnless(self.cssregistry.getResource('++resource++jquery.layout.plonekss.css') is not None)
        return


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite