# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\extra\pytz.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 2021 bytes
"""
----------------
hypothesis[pytz]
----------------

This module provides :pypi:`pytz` timezones.

You can use this strategy to make
:py:func:`hypothesis.strategies.datetimes` and
:py:func:`hypothesis.strategies.times` produce timezone-aware values.
"""
import datetime as dt, pytz
from pytz.tzfile import StaticTzInfo
import hypothesis.strategies._internal.core as st
__all__ = [
 'timezones']

@st.cacheable
@st.defines_strategy
def timezones() -> st.SearchStrategy[dt.tzinfo]:
    """Any timezone in the Olsen database, as a pytz tzinfo object.

    This strategy minimises to UTC, or the smallest possible fixed
    offset, and is designed for use with
    :py:func:`hypothesis.strategies.datetimes`.
    """
    all_timezones = [pytz.timezone(tz) for tz in pytz.all_timezones]
    static = [
     pytz.UTC]
    static += sorted((t for t in all_timezones if isinstance(t, StaticTzInfo)),
      key=(lambda tz: abs(tz.utcoffset(dt.datetime(2000, 1, 1)))))
    dynamic = [tz for tz in all_timezones if tz not in static]
    return st.sampled_from(static + dynamic)