# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/utils/dt.py
# Compiled at: 2016-11-29 01:45:48
__doc__ = '\n.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>\n'
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