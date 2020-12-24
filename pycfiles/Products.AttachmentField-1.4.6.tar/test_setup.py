# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /opt/Plone-4.3.7-was-4.2.1/zeocluster/src/Products.ATSuccessStory/Products/ATSuccessStory/tests/test_setup.py
# Compiled at: 2015-12-17 03:21:31
__doc__ = 'Test site setup\n'
import unittest
from Products.ATSuccessStory.tests.base import ATSuccessStoryTestCase
from Products.CMFCore.utils import getToolByName

class TestSetup(ATSuccessStoryTestCase):
    """Test cases for the generic setup of the product."""

    def afterSetUp(self):
        ids = self.portal.objectIds()

    def test_tools(self):
        ids = self.portal.objectIds()
        self.failUnless('archetype_tool' in ids)

    def test_types(self):
        ids = self.portal.portal_types.objectIds()
        self.failUnless('Document' in ids)

    def test_skins(self):
        ids = self.portal.portal_skins.objectIds()
        self.failUnless('plone_templates' in ids)

    def test_workflows(self):
        ids = self.portal.portal_workflow.objectIds()
        self.failUnless('plone_workflow' in ids)

    def test_workflowChains(self):
        getChain = self.portal.portal_workflow.getChainForPortalType
        self.failUnless('plone_workflow' in getChain('Document') or 'simple_publication_workflow' in getChain('Document'))


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite