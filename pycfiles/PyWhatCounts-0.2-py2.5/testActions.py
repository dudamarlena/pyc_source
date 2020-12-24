# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PyWhatCounts/tests/testActions.py
# Compiled at: 2009-05-13 06:43:53
"""Tests for methods that change a WC subscriber's settings in some way.
"""
import unittest
from PyWhatCounts.Wrapper import WCWrapper
from PyWhatCounts.exceptions import WCUserError, WCSystemError, WCAuthError
from config import TEST_REALM, TEST_KEY, TEST_DUMMY_USER, TEST_LIST

class testSubscribeUser(unittest.TestCase):
    """
    From subscribeUser:
       "We're not checking for valid email or list_id going in, but we'll check
        the response coming out of WC.

        We set force_sub so that users get signed up even if they had been
        *deleted* from the realm.  (Set mostly to ensure testing works.)
        
        Possible WC error messages (<angles> denote variables of some kind):
        
        Bad email address: (raises WCUserError)
        FAILURE: 1 record(s) processed. 0 users subscribed to list(s) <list_id> (0 total subscriptions)

        Bad list: (raises WCUserError)
        FAILURE: Error looking up list ids, one or more list ids specified do not belong to your realm
       "
    """

    def setUp(self):
        self.pwc = WCWrapper()
        self.pwc._setConnectionInfo(TEST_REALM, TEST_KEY)

    def testActuallySubscribesNewUser(self):
        pass

    def testAllowsMultipleSubscribes(self):
        """subscribeUser should not protest if we add the same user twice in a row"""
        self.pwc.subscribeUser(TEST_DUMMY_USER, TEST_LIST)
        self.failUnless(self.pwc.subscribeUser(TEST_DUMMY_USER, TEST_LIST))

    def testBonksOnBadEmail(self):
        """Raise a WCUserError if WhatCounts rejects an email addresses (they're not too picky, though)."""
        self.assertRaises(WCUserError, self.pwc.subscribeUser, 'foobar', TEST_LIST)

    def testBonksOnBadList(self):
        """If the list you supply isn't in your realm, we should raise a WCUserError"""
        self.assertRaises(WCUserError, self.pwc.subscribeUser, TEST_DUMMY_USER, '1')

    def testWithoutForceSubResubBonks(self):
        """Someone that has opted out or been deleted should fail to resubscribe
        through the Web API (and raise a WCUserError in the process) unless
        force_sub is set to '1'.
        """
        self.assertRaises(WCUserError, self.pwc.subscribeUser, TEST_DUMMY_USER, TEST_LIST, '0')

    def tearDown(self):
        try:
            self.pwc._deleteUser(TEST_DUMMY_USER)
        except WCUserError:
            pass


class testUnsubscribeUser(unittest.TestCase):
    """
    """

    def setUp(self):
        self.pwc = WCWrapper()
        self.pwc._setConnectionInfo(TEST_REALM, TEST_KEY)

    def testActuallyUnsubscribesUser(self):
        self.failUnless(self.pwc.subscribeUser(TEST_DUMMY_USER, TEST_LIST))
        self.failUnless(TEST_LIST in self.pwc._findUser(TEST_DUMMY_USER)['lists'])
        self.failUnless(self.pwc.unsubscribeUser(TEST_DUMMY_USER, TEST_LIST))
        self.failUnless(TEST_LIST not in self.pwc._findUser(TEST_DUMMY_USER)['lists'])

    def testUserStillExists(self):
        """The user should still exist in the realm after being unsubscribed"""
        self.failUnless(self.pwc.subscribeUser(TEST_DUMMY_USER, TEST_LIST))
        self.failUnless(self.pwc.unsubscribeUser(TEST_DUMMY_USER, TEST_LIST))
        self.failUnless(self.pwc._findUser(TEST_DUMMY_USER)['lists'] == [''])

    def testBonksOnBadEmail(self):
        """Raise a WCUserError if WhatCounts rejects an email addresses (they're not too picky, though)."""
        self.assertRaises(WCUserError, self.pwc.unsubscribeUser, 'foobar', TEST_LIST)

    def testBonksOnBadList(self):
        """If the list you supply isn't in your realm, we should raise a WCUserError"""
        self.assertRaises(WCUserError, self.pwc.unsubscribeUser, TEST_DUMMY_USER, '1')

    def tearDown(self):
        try:
            self.pwc._deleteUser(TEST_DUMMY_USER)
        except WCUserError:
            pass


class testUpdateEmailAddress(unittest.TestCase):
    """
    """

    def setUp(self):
        self.pwc = WCWrapper()
        self.pwc._setConnectionInfo(TEST_REALM, TEST_KEY)
        self.pwc.subscribeUser(TEST_DUMMY_USER, TEST_LIST)
        self.new_test_email = TEST_DUMMY_USER.replace('@', '1@')

    def testBadNewEmailBonksFunny(self):
        """WC returns an incorrect error message if the new email address is bad"""
        self.assertRaises(WCUserError, self.pwc.updateEmailAddress, TEST_DUMMY_USER, 'foo')

    def testBonksOnNonExistantUser(self):
        """We should raise a WCUserError for updates of users that don't exist"""
        self.pwc._deleteUser(TEST_DUMMY_USER)
        self.assertRaises(WCUserError, self.pwc.updateEmailAddress, TEST_DUMMY_USER, TEST_DUMMY_USER)

    def testActuallyChangesAddress(self):
        """Test of basic email update functionality"""
        self.pwc.updateEmailAddress(TEST_DUMMY_USER, self.new_test_email)
        self.assertRaises(WCUserError, self.pwc._findUser, TEST_DUMMY_USER)
        self.failUnless(TEST_LIST in self.pwc._findUser(self.new_test_email)['lists'])

    def tearDown(self):
        try:
            self.pwc._deleteUser(TEST_DUMMY_USER)
        except WCUserError:
            try:
                self.pwc._deleteUser(self.new_test_email)
            except WCUserError:
                pass


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testSubscribeUser))
    suite.addTest(makeSuite(testUnsubscribeUser))
    suite.addTest(makeSuite(testUpdateEmailAddress))
    return suite


if __name__ == '__main__':
    unittest.main()