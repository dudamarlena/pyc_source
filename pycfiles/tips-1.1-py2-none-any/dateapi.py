# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ab/projects/python/tips/build/lib/tips/dateapi.py
# Compiled at: 2015-12-27 15:53:28
"""Date related functions for tips.py project."""
import datetime, re

def _str_to_obj(date):
    """Convert date string into date object. Return False if not a date."""
    try:
        list = date.split('-')
        if len(list[0]) != 4:
            return False
        list = [ int(i) for i in list ]
        year, month, day = list
        return datetime.date(year, month, day)
    except (ValueError, AttributeError):
        return False


def _obj_to_str(date):
    """Convert date object into date string."""
    return date.isoformat()


def check_convert(date):
    """check if valid date. convert time ago to date if applicable."""
    result = _str_to_obj(date)
    if result:
        return _obj_to_str(result)
    else:
        if re.match('^(\\d+[dwy])+$', date):
            days = 0
            ago = re.split('([dwy])', date)
            del ago[-1]
            ago = [ (int(a), b) for a, b in zip(ago[0::2], ago[1::2]) ]
            for i in ago:
                if i[1] == 'd':
                    days += i[0]
                elif i[1] == 'w':
                    days += i[0] * 7
                else:
                    days += i[0] * 365

            return time_ago(days)
        return False


def range(start, end):
    """Take date strings as inputs. Return list of date strings in range."""
    if _str_to_obj(start) > _str_to_obj(end):
        start, end = end, start
    dates = []
    current, end = _str_to_obj(start), _str_to_obj(end)
    while current <= end:
        dates.append(_obj_to_str(current))
        current += datetime.timedelta(days=1)

    return dates


def time_ago(amount, units='days'):
    """
    Return date of 'amount' units of time ago. Defaults to days,
    can be weeks, months, or years. ('months' represents 30 days).
    """
    if units == 'months':
        units = 'days'
        amount = amount * 30
    arg = {units: amount}
    date = datetime.date.today()
    date -= datetime.timedelta(**arg)
    date = _obj_to_str(date)
    return date


def today():
    """Return date today."""
    return _obj_to_str(datetime.date.today())


def day(date):
    """Return day string e.g. "17". Takes date string or object as input."""
    if isinstance(date, datetime.date):
        date = _obj_to_str(date)
    if not _str_to_obj(date):
        return False
    return date.split('-')[2]


def weekday(date):
    """
    Return number representing weekday (e.g. Monday == 1, Sunday == 7).
    Takes date string or object as input.
    """
    if isinstance(date, str) or isinstance(date, unicode):
        date = _str_to_obj(date)
    return datetime.date.isoweekday(date)