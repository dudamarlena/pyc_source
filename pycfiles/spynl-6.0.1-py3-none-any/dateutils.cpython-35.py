# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/workspace/spynl-git/venv/src/spynl/spynl/main/dateutils.py
# Compiled at: 2017-01-16 09:58:52
# Size of source mod 2**32: 1877 bytes
"""
Functions for handling dates and times.
"""
from datetime import datetime
import dateutil.parser
from pytz import utc, timezone
from spynl.main.utils import get_request, get_settings, get_user_info

def now(tz=None):
    """Current time, with timezone localised."""
    return localize_date(datetime.utcnow(), tz=tz)


def date_format_str():
    """Get the date format from the .ini file, or set default."""
    return get_settings().get('spynl.date_format', '%Y-%m-%dT%H:%M:%S%z')


def date_to_str(when):
    """Convert date to string according to settings format"""
    return when.strftime(date_format_str())


def date_from_str(dstr):
    """"
    Parses a string to a date/time and adds current timezone if no timezone
    information is present.
    """
    _when = dateutil.parser.parse(dstr)
    if not _when.tzinfo:
        _when = utc.localize(_when)
    return _when


def localize_date(when, user_specific=True, tz=None):
    """
    Localises datetime objects to a time zone.
    If no time zone is explicitly given and also no time zone is found
    in or to be used from the user information, then system timezone is used.
    If 'when', the datetime object, has itself has no timezone info,
    then we assume it represents UTC time.
    """
    if not tz:
        tz = get_settings().get('spynl.date_systemtz', 'UTC')
        if user_specific:
            request = get_request()
            if request:
                user_info = get_user_info(request)
                if user_info.get('tz'):
                    tz = user_info.get('tz')
                if not when.tzinfo:
                    when = when.replace(tzinfo=utc)
                return when.astimezone(timezone(tz))