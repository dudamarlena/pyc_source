# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/taborc/git/spog/flask_extras/flask_extras/filters/datetimes.py
# Compiled at: 2017-03-03 15:46:17
"""Date and date-time related filters."""
from dateutil.parser import parse as dtparse

def str2dt(timestr):
    """Convert a string date to a real date.

    Args:
        timestr (str) - the datetime as a raw string.
    Returns:
        dateutil.parser.parse - the parsed datetime object.
    """
    return dtparse(timestr)