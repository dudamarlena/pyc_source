# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/metadata_client/tests/common/util_datetime.py
# Compiled at: 2017-06-19 07:48:53
# Size of source mod 2**32: 1813 bytes
"""UtilDatetimeFormat class"""
import unittest
from datetime import timezone, timedelta
from time import localtime

class UtilDatetime(unittest.TestCase):

    @staticmethod
    def datetime_to_local_timezone(dt):
        epoch = dt.timestamp()
        st_time = localtime(epoch)
        tz = timezone(timedelta(seconds=(st_time.tm_gmtoff)))
        dt_ltz = dt.astimezone(tz)
        return dt_ltz

    @staticmethod
    def datetime_to_local_tz_str(dt):
        dt_ltz = UtilDatetime.datetime_to_local_timezone(dt)
        dt_ltz_str = dt_ltz.isoformat()
        dt_ltz_str = dt_ltz_str[:-12] + '000' + dt_ltz_str[-6:]
        return dt_ltz_str

    @staticmethod
    def datetime_to_specific_timezone(dt, seconds_offset=7200):
        epoch = dt.timestamp()
        st_time = localtime(epoch)
        tz = timezone(timedelta(seconds=seconds_offset))
        dt_ltz = dt.astimezone(tz)
        return dt_ltz


if __name__ == '__main__':
    unittest.main()