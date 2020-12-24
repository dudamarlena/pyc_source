# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zeta/lib/datefmt.py
# Compiled at: 2010-01-24 10:23:28
"""
How DateTime is managed in Zeta ?
  * All date-time values are stored in database as UTC time zone.
  * When ever user provides a date-time value, it will be converted to
    UTC before storing them into the database.
  * Before rendering the date-time value from the data base to the client
    terminal, they will be converted to User's local time zone.
"""
import logging
from datetime import datetime, timedelta
from pytz import timezone, all_timezones, utc
import pytz
log = logging.getLogger(__name__)
is_tz = lambda tzname: tzname in pytz.all_timezones
utcnow = lambda : datetime.utcnow()

def usertz_2_utc(userdt, usertz=None):
    """User provided date-time value should be converted to UTC timezone.

    `userdt`  can be an `aware` instance of datetime.datetime. Otherwise
              `usertz` should be provided."""
    usertz = isinstance(usertz, (str, unicode)) and timezone(usertz) or usertz
    userdt = userdt.tzinfo and userdt or usertz.localize(userdt)
    utcdt = userdt.astimezone(timezone('UTC'))
    return utcdt


def utc_2_usertz(utcdt, usertz):
    """DateTime from database is in UTC timezone. Convert that into user
    timzone specifed by `usertz`.

    `utcdt`     can be an `aware` instance of datetime.datetime. Otherwise it
                will be localized to 'UTC' timezone.
    `usertz`    string or `tzinfo`.
    """
    usertz = isinstance(usertz, (str, unicode)) and timezone(usertz) or usertz
    utcdt = utcdt.tzinfo and utcdt or timezone('UTC').localize(utcdt)
    userdt = utcdt.astimezone(usertz)
    return userdt


def timeinfuture(somedt):
    """Check whether the passed DateTime instance is representing time in
    future or past.

    Return True, if the time is in future. Else False.
    """
    userdt = somedt.tzname() != 'UTC' and usertz_2_UTC(somedt) or somedt
    timelist = list(datetime.timetuple(datetime.utcnow()))[:7] + [
     timezone('UTC')]
    curr_udt = datetime(*timelist)
    diff = userdt - curr_udt
    if diff.days < 0 or diff.seconds < 0 or diff.microseconds < 0:
        return False
    else:
        return True