# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PyWhatCounts/tests/testHelperMethods.py
# Compiled at: 2009-05-13 06:43:53
"""Tests for our private helper methods.
"""
import unittest
from PyWhatCounts.Wrapper import WCWrapper
from PyWhatCounts.exceptions import WCUserError, WCSystemError, WCAuthError
from config import TEST_REALM, TEST_KEY, TEST_DUMMY_USER, TEST_LIST

class testFindUser(unittest.TestCase):
    """
    """

    def setUp(self):
        self.pwc = WCWrapper()
        self.pwc._setConnectionInfo(TEST_REALM, TEST_KEY)
        self.pwc.subscribeUser(TEST_DUMMY_USER, TEST_LIST)

    def testActuallyFindsUser(self):
        self.failUnless(self.pwc._findUser(TEST_DUMMY_USER)['email'] == TEST_DUMMY_USER)

    def testBonksOnNonExistantUser(self):
        """Raise a WCUserError if user doesn't exist in realm"""
        self.assertRaises(WCUserError, self.pwc._findUser, 'foo@bar.com')

    def tearDown(self):
        self.pwc._deleteUser(TEST_DUMMY_USER)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testFindUser))
    return suite


if __name__ == '__main__':
    unittest.main()