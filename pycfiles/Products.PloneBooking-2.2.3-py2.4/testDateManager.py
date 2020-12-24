# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Products\PloneBooking\tests\testDateManager.py
# Compiled at: 2008-11-19 15:29:07
"""
PloneBooking base test

$Id: testDateManager.py,v 1.7 2006/02/16 11:30:40 cbosse Exp $
"""
from DateTime import DateTime
from common import *
tests = []

class TestSecurity(PloneBookingTestCase):
    __module__ = __name__

    def testDateRangeFromWeek(self):
        """
        Test method getDateRangeFromWeek
        """
        (start_date, end_date) = self.btool.getDateRangeFromWeek(start_week=7, start_year=2004)
        self.assertEquals(DateTime(start_date.year(), start_date.month(), start_date.day()), DateTime(2004, 2, 9))
        self.assertEquals(end_date, DateTime(2004, 2, 15, 23, 59, 59))
        (start_date, end_date) = self.btool.getDateRangeFromWeek(start_week=4, start_year=2005)
        self.assertEquals(start_date, DateTime(2005, 1, 24, 0, 0, 0))
        self.assertEquals(end_date, DateTime(2005, 1, 30, 23, 59, 59))
        (start_date, end_date) = self.btool.getDateRangeFromWeek(start_week=7, start_year=2004, end_week=10)
        self.assertEquals(start_date, DateTime(2004, 2, 9))
        self.assertEquals(end_date, DateTime(2004, 3, 7, 23, 59, 59))

    def testDateRangeFromMonth(self):
        """
        Test method getDateRangeFromMonth
        """
        (start_date, end_date) = self.btool.getDateRangeFromMonth(start_month=2, start_year=2004)
        self.assertEquals(start_date, DateTime(2004, 2, 1))
        self.assertEquals(end_date, DateTime(2004, 2, 29, 23, 59, 59))
        (start_date, end_date) = self.btool.getDateRangeFromMonth(start_month=2, start_year=2004, end_month=3)
        self.assertEquals(start_date, DateTime(2004, 2, 1))
        self.assertEquals(end_date, DateTime(2004, 3, 31, 23, 59, 59))

    def testDateRangeFromYear(self):
        """
        Test method getDateRangeFromYear
        """
        (start_date, end_date) = self.btool.getDateRangeFromYear(start_year=2004)
        self.assertEquals(start_date, DateTime(2004, 1, 1))
        self.assertEquals(end_date, DateTime(2005, 1, 1))
        (start_date, end_date) = self.btool.getDateRangeFromYear(start_year=2004, end_year=2005)
        self.assertEquals(start_date, DateTime(2004, 1, 1))
        self.assertEquals(end_date, DateTime(2006, 1, 1))

    def testWeekDayNumberOfMonth(self):
        """
        test method weekDayNumberOfMonth
        """
        date = DateTime('2005/08/01')
        self.assertEquals(1, self.btool.weekDayNumberOfMonth(date))
        date = DateTime('2005/08/08')
        self.assertEquals(2, self.btool.weekDayNumberOfMonth(date))
        date = DateTime('2005/08/29')
        self.assertEquals(5, self.btool.weekDayNumberOfMonth(date))


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