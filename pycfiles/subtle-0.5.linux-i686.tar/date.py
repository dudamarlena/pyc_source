# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/guessit/date.py
# Compiled at: 2013-03-18 16:30:48
from __future__ import unicode_literals
import datetime, re

def valid_year(year):
    return 1920 < year < datetime.date.today().year + 5


def search_year(string):
    """Looks for year patterns, and if found return the year and group span.
    Assumes there are sentinels at the beginning and end of the string that
    always allow matching a non-digit delimiting the date.

    Note this only looks for valid production years, that is between 1920
    and now + 5 years, so for instance 2000 would be returned as a valid
    year but 1492 would not.

    >>> search_year('in the year 2000...')
    (2000, (12, 16))

    >>> search_year('they arrived in 1492.')
    (None, None)
    """
    match = re.search(b'[^0-9]([0-9]{4})[^0-9]', string)
    if match:
        year = int(match.group(1))
        if valid_year(year):
            return (year, match.span(1))
    return (None, None)


def search_date(string):
    """Looks for date patterns, and if found return the date and group span.
    Assumes there are sentinels at the beginning and end of the string that
    always allow matching a non-digit delimiting the date.

    >>> search_date('This happened on 2002-04-22.')
    (datetime.date(2002, 4, 22), (17, 27))

    >>> search_date('And this on 17-06-1998.')
    (datetime.date(1998, 6, 17), (12, 22))

    >>> search_date('no date in here')
    (None, None)
    """
    dsep = b'[-/ \\.]'
    date_rexps = [
     b'[^0-9]' + b'(?P<year>[0-9]{4})' + b'(?P<month>[0-9]{2})' + b'(?P<day>[0-9]{2})' + b'[^0-9]',
     b'[^0-9]' + b'(?P<year>[0-9]{4})' + dsep + b'(?P<month>[0-9]{2})' + dsep + b'(?P<day>[0-9]{2})' + b'[^0-9]',
     b'[^0-9]' + b'(?P<day>[0-9]{2})' + dsep + b'(?P<month>[0-9]{2})' + dsep + b'(?P<year>[0-9]{4})' + b'[^0-9]',
     b'[^0-9]' + b'(?P<day>[0-9]{2})' + dsep + b'(?P<month>[0-9]{2})' + dsep + b'(?P<year>[0-9]{2})' + b'[^0-9]']
    for drexp in date_rexps:
        match = re.search(drexp, string)
        if match:
            d = match.groupdict()
            year, month, day = int(d[b'year']), int(d[b'month']), int(d[b'day'])
            if year < 100:
                if year > datetime.date.today().year % 100 + 5:
                    year = 1900 + year
                else:
                    year = 2000 + year
            date = None
            try:
                date = datetime.date(year, month, day)
            except ValueError:
                try:
                    date = datetime.date(year, day, month)
                except ValueError:
                    pass

            if date is None:
                continue
            if not 1900 < date.year < datetime.date.today().year + 5:
                continue
            start, end = match.span()
            return (
             date, (start + 1, end - 1))

    return (None, None)