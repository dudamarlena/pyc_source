# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\Products\PloneBooking\tests\testSecurity.py
# Compiled at: 2008-11-19 15:29:07
__doc__ = '\nPloneBooking base test\n\n$Id: testSecurity.py,v 1.4 2006/02/16 11:30:40 cbosse Exp $\n'
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