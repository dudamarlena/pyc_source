# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/collective/listjs/tests/test_integration_unit.py
# Compiled at: 2011-11-01 10:41:40
__doc__ = 'This is an integration "unit" test. It uses PloneTestCase, but does not\nuse doctest syntax.\n\nYou will find lots of examples of this type of test in CMFPlone/tests, for \nexample.\n'
import unittest
from collective.listjs.tests.base import ExampleTestCase
from Products.CMFCore.utils import getToolByName

class TestSetup(ExampleTestCase):
    """The name of the class should be meaningful. This may be a class that
    tests the installation of a particular product.
    """

    def afterSetUp(self):
        """This method is called before each single test. It can be used to
        set up common state. Setup that is specific to a particular test 
        should be done in that test method.
        """
        self.workflow = getToolByName(self.portal, 'portal_workflow')

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

    def test_portal_title(self):
        self.assertEquals('Plone site', self.portal.getProperty('title'))

    def test_able_to_add_document(self):
        new_id = self.folder.invokeFactory('Document', 'my-page')
        self.assertEquals('my-page', new_id)


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite