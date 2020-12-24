# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pg_python2/pg_time.py
# Compiled at: 2018-06-20 09:55:01
# Size of source mod 2**32: 1027 bytes
from datetime import datetime, timedelta
import pytz, time, calendar

def _utc_to_local(utc_dt, tz):
    local_dt = utc_dt.replace(tzinfo=(pytz.utc)).astimezone(tz)
    return tz.normalize(local_dt)


def get_ist_date():
    india = pytz.timezone('Asia/Kolkata')
    x = _utc_to_local(datetime.utcnow(), india)
    return x.strftime('%Y-%m-%d')


def get_ist_time():
    india = pytz.timezone('Asia/Kolkata')
    x = _utc_to_local(datetime.utcnow(), india)
    return x.strftime('%H:%M:%S')


def get_ist_datetime():
    india = pytz.timezone('Asia/Kolkata')
    x = _utc_to_local(datetime.utcnow(), india)
    return x.strftime('%Y%m%d%H%M%S')


def get_hawker_date(day_gap):
    india = pytz.timezone('Asia/Kolkata')
    x = _utc_to_local(datetime.utcnow(), india)
    if day_gap != 0:
        x = _utc_to_local(datetime.utcnow() - timedelta(days=day_gap), india)
    return x.strftime('%Y%m%d')


def get_epoch_date(hawker_time):
    t = time.strptime(hawker_time, '%Y%m%d%H%M%S')
    return int(calendar.timegm(t) / 60)