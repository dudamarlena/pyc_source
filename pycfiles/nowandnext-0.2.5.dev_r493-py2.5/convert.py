# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nowandnext/calendar/convert.py
# Compiled at: 2009-05-11 19:02:39
import datetime
from nowandnext.calendar import periods

def timedelta_to_seconds(td):
    assert isinstance(td, datetime.timedelta)
    return td.days * periods.SECONDS_IN_A_DAY + td.seconds


def timedelta_to_minutes(td):
    return timedelta_to_seconds(td) / float(periods.SECONDS_IN_A_MINUTE)


if __name__ == '__main__':
    start = datetime.datetime(2008, 3, 1)
    end = datetime.datetime(2008, 3, 2)
    delta = end - start
    print timedelta_to_minutes(delta)