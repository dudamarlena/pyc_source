# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PyWhatCounts/tests/testQueries.py
# Compiled at: 2009-05-13 06:43:53
"""Tests for methods that ask WC for realm-level or user-related data.
"""
import unittest
from PyWhatCounts.Wrapper import WCWrapper
from PyWhatCounts.exceptions import WCUserError, WCSystemError, WCAuthError
from config import TEST_REALM, TEST_KEY, TEST_DUMMY_USER, TEST_LIST

class testShowLists(unittest.TestCase):
    """
    Show lists should be pretty bomber; it just takes a realm and pwd.
    """

    def setUp(self):
        self.pwc = WCWrapper()
        self.pwc._setConnectionInfo(TEST_REALM, TEST_KEY)

    def testShowLists(self):
        """Make sure that the TEST_LIST is among the results of the realm's lists"""
        list_ids = [ l[0] for l in self.pwc.showLists() ]
        self.failUnless(TEST_LIST in list_ids)

    def testFailsWithBadCreds(self):
        """Make sure we raise an exception with bad user name/pass"""
        self.pwc._setConnectionInfo(TEST_REALM, '123')
        self.assertRaises(WCAuthError, self.pwc.showLists)
        self.pwc._setConnectionInfo('whatcounts', TEST_KEY)
        self.assertRaises(WCAuthError, self.pwc.showLists)


class testGetUserDetails(unittest.TestCase):
    """
    
    """

    def setUp(self):
        self.pwc = WCWrapper()
        self.pwc._setConnectionInfo(TEST_REALM, TEST_KEY)
        self.pwc.subscribeUser(TEST_DUMMY_USER, TEST_LIST)

    def testGetsDetails(self):
        """Basic func test"""
        dummy = self.pwc.getUserDetails(TEST_DUMMY_USER)
        self.failUnless(dummy['email'] == TEST_DUMMY_USER)

    def testBonksOnNonExistantUser(self):
        """If the user doesn't exist, raise a WCUserError"""
        self.assertRaises(WCUserError, self.pwc.getUserDetails, 'bogus@onenw.org')

    def tearDown(self):
        self.pwc._deleteUser(TEST_DUMMY_USER)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testShowLists))
    suite.addTest(makeSuite(testGetUserDetails))
    return suite


if __name__ == '__main__':
    unittest.main()