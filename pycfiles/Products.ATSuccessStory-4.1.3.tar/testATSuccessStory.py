# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/Plone-4.3.7-was-4.2.1/zeocluster/src/Products.ATSuccessStory/Products/ATSuccessStory/tests/testATSuccessStory.py
# Compiled at: 2015-12-17 03:21:31
import unittest, doctest
from Products.ATSuccessStory.content.ATSuccessStory import ATSuccessStory
from Products.ATSuccessStory.tests.base import ATSuccessStoryTestCase, ATSuccessStoryFunctionalTestCase
from Products.CMFCore.utils import getToolByName
from Testing import ZopeTestCase as ztc

class testATSuccessStory(ATSuccessStoryTestCase):
    """Test-cases for class(es) ATSuccessStory."""

    def afterSetUp(self):
        self.pt = getToolByName(self.portal, 'portal_types')

    def testOnlyInATSSFolder(self):
        self.failIf(self.pt.ATSuccessStory.global_allow, 'Success stories are globally addable')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testATSuccessStory))
    suite.addTest(ztc.ZopeDocFileSuite('testATSSfunctional.txt', package='Products.ATSuccessStory.tests', test_class=ATSuccessStoryFunctionalTestCase, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS))
    return suite


if __name__ == '__main__':
    framework()