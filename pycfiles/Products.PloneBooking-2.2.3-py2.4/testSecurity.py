# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Products\PloneBooking\tests\testSecurity.py
# Compiled at: 2008-11-19 15:29:07
"""
PloneBooking base test

$Id: testSecurity.py,v 1.4 2006/02/16 11:30:40 cbosse Exp $
"""
from DateTime import DateTime
from common import *
from Products.CMFCore.utils import getToolByName
tests = []

class TestSecurity(PloneBookingTestCase):
    __module__ = __name__

    def testCheckPermissions(self):
        """
        Check permissions
        """
        self.loginAsPortalMember()
        permissions = (
         BookingPermissions.AddBookingCenter, BookingPermissions.AddBookableObject)
        for permission in permissions:
            self.failUnless(not self.mbtool.checkPermission(permission, self.portal))
            self.failUnless(self.mbtool.checkPermission(permission, self.member_folder))

        permissions = (BookingPermissions.AddBooking,)
        for permission in permissions:
            self.failUnless(self.mbtool.checkPermission(permission, self.portal))

        self.logout()


tests.append(TestSecurity)
if __name__ == '__main__':
    framework()
else:
    import unittest

    def test_suite():
        suite = unittest.TestSuite()
        for test in tests:
            suite.addTest(unittest.makeSuite(test))

        return suite