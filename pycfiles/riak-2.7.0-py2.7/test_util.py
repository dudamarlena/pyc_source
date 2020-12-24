# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: py-build/2.7/bdist.linux-x86_64/egg/riak/tests/test_util.py
# Compiled at: 2016-10-17 19:06:50
import datetime, unittest
from riak.util import is_timeseries_supported, datetime_from_unix_time_millis, unix_time_millis

class UtilUnitTests(unittest.TestCase):

    def test_conv_ms_timestamp_to_datetime_and_back(self):
        if is_timeseries_supported():
            v = 144379690987
            dt = datetime_from_unix_time_millis(v)
            utp = 144379690.987
            dtp = datetime.datetime.utcfromtimestamp(utp)
            self.assertEqual(dt, dtp)
            utm = unix_time_millis(dt)
            self.assertEqual(v, utm)

    def test_conv_datetime_to_unix_millis(self):
        if is_timeseries_supported():
            v = 144379690.987
            d = datetime.datetime.utcfromtimestamp(v)
            utm = unix_time_millis(d)
            self.assertEqual(utm, 144379690987)

    def test_unix_millis_validation(self):
        v = 144379690.987
        with self.assertRaises(ValueError):
            datetime_from_unix_time_millis(v)

    def test_unix_millis_small_value(self):
        if is_timeseries_supported():
            v = 1001
            dt = datetime_from_unix_time_millis(v)
            utp = 1.001
            dtp = datetime.datetime.utcfromtimestamp(utp)
            self.assertEqual(dt, dtp)
            utm = unix_time_millis(dt)
            self.assertEqual(v, utm)

    def test_is_timeseries_supported(self):
        v = (2, 7, 10)
        self.assertEqual(True, is_timeseries_supported(v))
        v = (2, 7, 11)
        self.assertEqual(True, is_timeseries_supported(v))
        v = (2, 7, 12)
        self.assertEqual(True, is_timeseries_supported(v))
        v = (3, 3, 6)
        self.assertEqual(False, is_timeseries_supported(v))
        v = (3, 4, 3)
        self.assertEqual(False, is_timeseries_supported(v))
        v = (3, 4, 4)
        self.assertEqual(True, is_timeseries_supported(v))
        v = (3, 4, 5)
        self.assertEqual(True, is_timeseries_supported(v))
        v = (3, 5, 0)
        self.assertEqual(False, is_timeseries_supported(v))
        v = (3, 5, 1)
        self.assertEqual(True, is_timeseries_supported(v))