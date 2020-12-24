# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/lib/utils/time.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 3258 bytes
"""
Date & Time related utilities
"""
import datetime, dateparser
from dateutil.tz import tzutc

def timestamp_to_iso(timestamp):
    """
    Convert Unix Epoch Timestamp to ISO formatted time string:
        Ex: 1234567890 -> 2018-07-05T03:09:43.842000

    Parameters
    ----------
    timestamp : int
        Unix epoch timestamp

    Returns
    -------
    str
        ISO formatted time string
    """
    return to_datetime(timestamp).isoformat()


def to_datetime(timestamp):
    """
    Convert Unix Epoch Timestamp to Python's ``datetime.datetime`` object

    Parameters
    ----------
    timestamp : int
        Unix epoch timestamp

    Returns
    -------
    datetime.datetime
        Datetime representation of timestamp
    """
    timestamp_secs = int(timestamp) / 1000.0
    return datetime.datetime.utcfromtimestamp(timestamp_secs)


def to_timestamp(some_time):
    """
    Converts the given datetime value to Unix timestamp

    Parameters
    ----------
    some_time : datetime.datetime
        Value to be converted to unix epoch. This must be without any timezone identifier

    Returns
    -------
    int
        Unix timestamp of the given time
    """
    return int((some_time - datetime.datetime(1970, 1, 1)).total_seconds() * 1000.0)


def utc_to_timestamp(utc):
    """
    Converts utc timestamp with tz_info set to utc to Unix timestamp
    :param utc: datetime.datetime
    :return: UNIX timestamp
    """
    return to_timestamp(utc.replace(tzinfo=None))


def to_utc(some_time):
    """
    Convert the given date to UTC, if the date contains a timezone.

    Parameters
    ----------
    some_time : datetime.datetime
        datetime object to convert to UTC

    Returns
    -------
    datetime.datetime
        Converted datetime object
    """
    if some_time.tzinfo:
        if some_time.utcoffset():
            some_time = some_time.astimezone(tzutc())
    return some_time.replace(tzinfo=None)


def parse_date(date_string):
    """
    Parse the given string as datetime object. This parser supports in almost any string formats.

    For relative times, like `10min ago`, this parser computes the actual time relative to current UTC time. This
    allows time to always be in UTC if an explicit time zone is not provided.

    Parameters
    ----------
    date_string : str
        String representing the date

    Returns
    -------
    datetime.datetime
        Parsed datetime object. None, if the string cannot be parsed.
    """
    parser_settings = {'RELATIVE_BASE': datetime.datetime.utcnow()}
    return dateparser.parse(date_string, settings=parser_settings)