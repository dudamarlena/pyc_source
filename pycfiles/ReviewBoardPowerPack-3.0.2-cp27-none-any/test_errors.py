# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /beanbag_licensing/tests/test_errors.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
from djblets.testing.testcases import TestCase
from beanbag_licensing.errors import TooManyUsersForLicenseError

class TooManyUsersForLicenseErrorTests(TestCase):
    """Unit tests for TooManyUsersForLicenseError."""

    def test_0_remaining(self):
        """Testing TooManyUsersForLicenseError with 0 users remaining"""
        e = TooManyUsersForLicenseError(5, 0)
        self.assertEqual(str(e), b'Unable to add additional users to the license. The license user cap has been hit.')

    def test_1_remaining(self):
        """Testing TooManyUsersForLicenseError with 1 user remaining"""
        e = TooManyUsersForLicenseError(5, 1)
        self.assertEqual(str(e), b'Unable to add 5 additional users to the license. The license only has room for 1 more user.')

    def test_gt_1_remaining(self):
        """Testing TooManyUsersForLicenseError with > 1 user remaining"""
        e = TooManyUsersForLicenseError(3, 2)
        self.assertEqual(str(e), b'Unable to add 3 additional users to the license. The license only has room for 2 more users.')