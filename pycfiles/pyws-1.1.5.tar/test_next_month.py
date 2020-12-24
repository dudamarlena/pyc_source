# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stepank/projects/pyws/tests/python/suds/testcases/test_next_month.py
# Compiled at: 2013-11-29 15:32:12
import unittest2 as unittest
from datetime import date, datetime
from testcases.base import BaseTestCaseMixin

class NextMonthTestCase(BaseTestCaseMixin, unittest.TestCase):

    def test_simple(self):
        self.assertEqual(self.service.next_month(date(2011, 8, 20)), date(2011, 9, 20))

    def test_dt(self):
        self.assertEqual(self.service.next_month_dt(datetime(2011, 8, 20, 0, 4, 59, 123)), datetime(2011, 9, 20, 0, 4, 59, 123))