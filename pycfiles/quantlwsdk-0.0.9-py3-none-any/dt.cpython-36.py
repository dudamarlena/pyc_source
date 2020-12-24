# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\pyalgotrade\utils\dt.py
# Compiled at: 2019-06-05 03:26:22
# Size of source mod 2**32: 2481 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import datetime, pytz

def datetime_is_naive(dateTime):
    """ Returns True if dateTime is naive."""
    return dateTime.tzinfo is None or dateTime.tzinfo.utcoffset(dateTime) is None


def unlocalize(dateTime):
    return dateTime.replace(tzinfo=None)


def localize(dateTime, timeZone):
    """Returns a datetime adjusted to a timezone:

     * If dateTime is a naive datetime (datetime with no timezone information), timezone information is added but date
       and time remains the same.
     * If dateTime is not a naive datetime, a datetime object with new tzinfo attribute is returned, adjusting the date
       and time data so the result is the same UTC time.
    """
    if datetime_is_naive(dateTime):
        ret = timeZone.localize(dateTime)
    else:
        ret = dateTime.astimezone(timeZone)
    return ret


def as_utc(dateTime):
    return localize(dateTime, pytz.utc)


def datetime_to_timestamp(dateTime):
    """ Converts a datetime.datetime to a UTC timestamp."""
    diff = as_utc(dateTime) - epoch_utc
    return diff.total_seconds()


def timestamp_to_datetime(timeStamp, localized=True):
    """ Converts a UTC timestamp to a datetime.datetime."""
    ret = datetime.datetime.utcfromtimestamp(timeStamp)
    if localized:
        ret = localize(ret, pytz.utc)
    return ret


def get_first_monday(year):
    ret = datetime.date(year, 1, 1)
    if ret.weekday() != 0:
        diff = 7 - ret.weekday()
        ret = ret + datetime.timedelta(days=diff)
    return ret


def get_last_monday(year):
    ret = datetime.date(year, 12, 31)
    if ret.weekday() != 0:
        diff = ret.weekday() * -1
        ret = ret + datetime.timedelta(days=diff)
    return ret


epoch_utc = as_utc(datetime.datetime(1970, 1, 1))