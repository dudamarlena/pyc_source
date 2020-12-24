# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/substrate/data/lib/substrate/agar/dates.py
# Compiled at: 2012-02-03 19:38:43
"""
The ``agar.dates`` module contains a function to help work with dates.
"""
import re
from datetime import datetime, timedelta
from pytz.gae import pytz

def parse_datetime(s):
    """
    Create ``datetime`` object representing date/time expressed in a string.

    Takes a string in the format produced by calling ``str()``
    on a python ``datetime`` object and returns a ``datetime``
    instance that would produce that string.

    Acceptable formats are:

     * ``YYYY-MM-DD HH:MM:SS.ssssss+HH:MM``
     * ``YYYY-MM-DD HH:MM:SS.ssssss``
     * ``YYYY-MM-DD HH:MM:SS+HH:MM``
     * ``YYYY-MM-DD HH:MM:SS``
     * ``YYYY-MM-DD``

    Where ``ssssss`` represents fractional seconds.  The timezone
    is optional and may be either positive or negative
    hours/minutes east of UTC.

    :param s: The string to parse into a ``datetime``.
    :return: The ``datetime`` represented by the given string.
    """
    if s is None:
        return
    else:
        m = re.match('(.*?)(?:\\.(\\d+))?(([-+]\\d{1,2}):(\\d{2}))?$', str(s))
        datestr, fractional, tzname, tzhour, tzmin = m.groups()
        if tzname is None:
            tz = None
        else:
            tzhour, tzmin = int(tzhour), int(tzmin)
            if tzhour == tzmin == 0:
                tzname = 'UTC'
            tz = pytz.reference.FixedOffset(timedelta(hours=tzhour, minutes=tzmin), tzname)
        try:
            x = datetime.strptime(datestr, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            x = datetime.strptime(datestr, '%Y-%m-%d')

        if fractional is None:
            fractional = '0'
        fracpower = 6 - len(fractional)
        fractional = float(fractional) * 10 ** fracpower
        return x.replace(microsecond=int(fractional), tzinfo=tz)