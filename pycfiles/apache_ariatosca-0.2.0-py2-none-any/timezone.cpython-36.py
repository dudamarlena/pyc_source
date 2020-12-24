# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/utils/timezone.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 5193 bytes
import datetime as dt, pendulum
from airflow.settings import TIMEZONE
utc = pendulum.timezone('UTC')

def is_localized(value):
    """
    Determine if a given datetime.datetime is aware.
    The concept is defined in Python's docs:
    http://docs.python.org/library/datetime.html#datetime.tzinfo
    Assuming value.tzinfo is either None or a proper datetime.tzinfo,
    value.utcoffset() implements the appropriate logic.
    """
    return value.utcoffset() is not None


def is_naive(value):
    """
    Determine if a given datetime.datetime is naive.
    The concept is defined in Python's docs:
    http://docs.python.org/library/datetime.html#datetime.tzinfo
    Assuming value.tzinfo is either None or a proper datetime.tzinfo,
    value.utcoffset() implements the appropriate logic.
    """
    return value.utcoffset() is None


def utcnow():
    """
    Get the current date and time in UTC
    :return:
    """
    d = dt.datetime.utcnow()
    d = d.replace(tzinfo=utc)
    return d


def utc_epoch():
    """
    Gets the epoch in the users timezone
    :return:
    """
    d = dt.datetime(1970, 1, 1)
    d = d.replace(tzinfo=utc)
    return d


def convert_to_utc(value):
    """
    Returns the datetime with the default timezone added if timezone
    information was not associated
    :param value: datetime
    :return: datetime with tzinfo
    """
    if not value:
        return value
    else:
        if not is_localized(value):
            value = pendulum.instance(value, TIMEZONE)
        return value.astimezone(utc)


def make_aware(value, timezone=None):
    """
    Make a naive datetime.datetime in a given time zone aware.

    :param value: datetime
    :param timezone: timezone
    :return: localized datetime in settings.TIMEZONE or timezone

    """
    if timezone is None:
        timezone = TIMEZONE
    else:
        if is_localized(value):
            raise ValueError('make_aware expects a naive datetime, got %s' % value)
        if hasattr(value, 'fold'):
            value = value.replace(fold=1)
    if hasattr(timezone, 'localize'):
        return timezone.localize(value)
    else:
        if hasattr(timezone, 'convert'):
            return timezone.convert(value)
        return value.replace(tzinfo=timezone)


def make_naive(value, timezone=None):
    """
    Make an aware datetime.datetime naive in a given time zone.

    :param value: datetime
    :param timezone: timezone
    :return: naive datetime
    """
    if timezone is None:
        timezone = TIMEZONE
    if is_naive(value):
        raise ValueError('make_naive() cannot be applied to a naive datetime')
    o = value.astimezone(timezone)
    naive = dt.datetime(o.year, o.month, o.day, o.hour, o.minute, o.second, o.microsecond)
    return naive


def datetime(*args, **kwargs):
    """
    Wrapper around datetime.datetime that adds settings.TIMEZONE if tzinfo not specified

    :return: datetime.datetime
    """
    if 'tzinfo' not in kwargs:
        kwargs['tzinfo'] = TIMEZONE
    return (dt.datetime)(*args, **kwargs)


def parse(string, timezone=None):
    """
    Parse a time string and return an aware datetime
    :param string: time string
    """
    return pendulum.parse(string, tz=(timezone or TIMEZONE))