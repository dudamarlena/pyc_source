# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/djutils/date_utils.py
# Compiled at: 2015-12-30 10:00:00
import calendar
from random import randrange
import datetime

def date_to_datetime(date):
    if date:
        return datetime.datetime(*date.timetuple()[:6])
    else:
        return
        return


def date_to_datetime_lte(date):
    return datetime.datetime.combine(date, datetime.time(23, 59, 59))


def iso_to_date(date_iso):
    if date_iso:
        return datetime.datetime.strptime(date_iso[:10], '%Y-%m-%d').date()
    else:
        return
        return


def iso_to_datetime(datetime_iso):
    if datetime_iso:
        return datetime.datetime.strptime(datetime_iso, '%Y-%m-%d %H:%M:%S')
    else:
        return
        return


def rus_to_date(date_rus):
    if date_rus:
        return datetime.datetime.strptime(date_rus, '%d.%m.%Y').date()
    else:
        return
        return


def date_to_timestamp(date):
    """
        date to unix timestamp in milliseconds
    """
    date_tuple = date.timetuple()
    timestamp = calendar.timegm(date_tuple) * 1000
    return timestamp


def random_date(dt_from, dt_to):
    """
    This function will return a random datetime between two datetime objects.
    :param start:
    :param end:
    """
    delta = dt_to - dt_from
    int_delta = delta.days * 24 * 60 * 60 + delta.seconds
    random_second = randrange(int_delta)
    return dt_from + datetime.timedelta(seconds=random_second)


def convert_timedelta_to_datetime(duration):
    return datetime.datetime.min + duration