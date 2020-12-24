# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/Plone-4.3.7-was-4.2.1/zeocluster/src/Products.ATSuccessStory/Products/ATSuccessStory/tests/testATSuccessStoryFolder.py
# Compiled at: 2015-12-17 03:21:31
import unittest
from Products.ATSuccessStory.content.ATSuccessStoryFolder import ATSuccessStoryFolder
from Products.ATSuccessStory.tests.base import ATSuccessStoryTestCase, ATSuccessStoryFunctionalTestCase
from Products.CMFCore.utils import getToolByName

class testATSuccessStoryFolder(ATSuccessStoryTestCase):
    """Test-cases for class(es) ATSuccessStoryFolder."""

    def afterSetUp(self):
        self.pt = getToolByName(self.portal, 'portal_types')

    def testOnlyAllowSS(self):
        self.assertEquals(self.pt.ATSuccessStoryFolder.allowed_content_types, ('ATSuccessStory', ), 'ATSuccessStoryFolder is allowing %s types' % str(self.pt.ATSuccessStoryFolder.allowed_content_types))

    def testDefaultView(self):
        self.assertEquals(self.pt.ATSuccessStoryFolder.default_view, 'summary_view', 'Default view for ATSuccessStoryFolder is not "summary_view"')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testATSuccessStoryFolder))
    return suite


if __name__ == '__main__':
    framework()