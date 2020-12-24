# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/ggplot/scales/date_utils.py
# Compiled at: 2016-07-31 11:30:58
from __future__ import absolute_import, division, print_function, unicode_literals
from matplotlib.dates import DateFormatter
from matplotlib.dates import MinuteLocator, HourLocator, DayLocator
from matplotlib.dates import WeekdayLocator, MonthLocator, YearLocator

def date_format(format=b'%Y-%m-%d', tz=None):
    """
    Format dates

    Parameters
    ----------
    format:
        Date format using standard strftime format.
    tz:
        Instance of datetime.tzinfo

    Examples
    --------
    >>> date_format('%b-%y')
    >>> date_format('%B %d, %Y')
    """
    return DateFormatter(format, tz)


def parse_break_str(txt):
    """parses '10 weeks' into tuple (10, week)."""
    txt = txt.strip()
    if len(txt.split()) == 2:
        n, units = txt.split()
    else:
        n, units = 1, txt
    units = units.rstrip(b's')
    n = int(n)
    return (n, units)


LOCATORS = {b'minute': MinuteLocator, 
   b'hour': HourLocator, 
   b'day': DayLocator, 
   b'week': WeekdayLocator, 
   b'month': MonthLocator, 
   b'year': lambda interval: YearLocator(base=interval)}

def date_breaks(width):
    """
    Regularly spaced dates

    Parameters
    ----------
    width:
        an interval specification. must be one of [minute, hour, day, week, month, year]

    Examples
    --------
    >>> date_breaks(width = '1 year')
    >>> date_breaks(width = '6 weeks')
    >>> date_breaks('months')
    """
    period, units = parse_break_str(width)
    Locator = LOCATORS.get(units)
    locator = Locator(interval=period)
    return locator