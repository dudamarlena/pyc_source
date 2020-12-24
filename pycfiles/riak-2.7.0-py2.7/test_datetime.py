# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: py-build/2.7/bdist.linux-x86_64/egg/riak/tests/test_datetime.py
# Compiled at: 2016-10-17 19:06:50
import datetime, unittest
from riak.util import epoch, epoch_tz, unix_time_millis
ts0 = datetime.datetime(2015, 1, 1, 12, 1, 2, 987000)
ts0_ts = 1420113662987
ts0_ts_pst = 1420142462987

class DatetimeUnitTests(unittest.TestCase):

    def test_get_unix_time_without_tzinfo(self):
        self.assertIsNone(epoch.tzinfo)
        self.assertIsNotNone(epoch_tz.tzinfo)
        self.assertIsNone(ts0.tzinfo)
        utm = unix_time_millis(ts0)
        self.assertEqual(utm, ts0_ts)

    def test_get_unix_time_with_tzinfo(self):
        try:
            import pytz
            tz = pytz.timezone('America/Los_Angeles')
            ts0_pst = tz.localize(ts0)
            utm = unix_time_millis(ts0_pst)
            self.assertEqual(utm, ts0_ts_pst)
        except ImportError:
            pass