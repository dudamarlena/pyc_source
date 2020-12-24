# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: rolex/__init__.py
# Compiled at: 2019-01-28 15:42:56
__version__ = '0.0.8'
__short_description__ = 'An elegant datetime library.'
__license__ = 'MIT'
__author__ = 'Sanhe Hu'
__author_email__ = 'husanhe@gmail.com'
__maintainer__ = 'Sanhe Hu'
__maintainer_email__ = 'husanhe@gmail.com'
__github_username__ = 'MacHu-GWU'
try:
    from .generator import time_series, weekday_series, rnd_date, rnd_date_array, rnd_datetime, rnd_datetime_array
    from .math import add_seconds, add_minutes, add_hours, add_days, add_weeks, add_months, add_years, round_to
    from .parse import parser
    str2date = parser.str2date
    str2datetime = parser.str2datetime
    parse_date = parser.parse_date
    parse_datetime = parser.parse_datetime
    from .tz import utc, local
    from .util import to_ordinal, from_ordinal, to_utctimestamp, from_utctimestamp, to_utc, utc_to_tz, utc_to_local
except ImportError:
    pass