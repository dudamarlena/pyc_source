# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Products/AnonymousCommenting/tests/test_anonymousCommenting.py
# Compiled at: 2009-01-12 12:00:07
__author__ = 'WebLion <support@weblion.psu.edu>'
__docformat__ = 'plaintext'
from Products.CMFCore.utils import getToolByName
import Products.AnonymousCommenting
from Products.AnonymousCommenting.tests.base import AnonymousCommentingTestCase

class testAnonymousCommenting(AnonymousCommentingTestCase):
    __module__ = __name__

    def test_anonymousCommentingEnabled(self):
        self.failUnless('Anonymous' in self.portal._Reply_to_item_Permission, "The Anonymous role does not have the 'Reply to item' permission.")

    def test_nameOnForm(self):
        self.failUnless('value="test_user_1_"' in self.portal['front-page']['discussion_reply_form'](), "The logged in user's name was not included in the comment form's name field.")


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testAnonymousCommenting))
    return suite