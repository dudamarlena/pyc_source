# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/utils/dateparse.py
# Compiled at: 2019-02-14 00:35:17
"""Functions to parse datetime objects."""
import datetime, re
from django.utils import six
from django.utils.timezone import get_fixed_timezone, utc
date_re = re.compile('(?P<year>\\d{4})-(?P<month>\\d{1,2})-(?P<day>\\d{1,2})$')
time_re = re.compile('(?P<hour>\\d{1,2}):(?P<minute>\\d{1,2})(?::(?P<second>\\d{1,2})(?:\\.(?P<microsecond>\\d{1,6})\\d{0,6})?)?')
datetime_re = re.compile('(?P<year>\\d{4})-(?P<month>\\d{1,2})-(?P<day>\\d{1,2})[T ](?P<hour>\\d{1,2}):(?P<minute>\\d{1,2})(?::(?P<second>\\d{1,2})(?:\\.(?P<microsecond>\\d{1,6})\\d{0,6})?)?(?P<tzinfo>Z|[+-]\\d{2}(?::?\\d{2})?)?$')
standard_duration_re = re.compile('^(?:(?P<days>-?\\d+) (days?, )?)?((?:(?P<hours>-?\\d+):)(?=\\d+:\\d+))?(?:(?P<minutes>-?\\d+):)?(?P<seconds>-?\\d+)(?:\\.(?P<microseconds>\\d{1,6})\\d{0,6})?$')
iso8601_duration_re = re.compile('^(?P<sign>[-+]?)P(?:(?P<days>\\d+(.\\d+)?)D)?(?:T(?:(?P<hours>\\d+(.\\d+)?)H)?(?:(?P<minutes>\\d+(.\\d+)?)M)?(?:(?P<seconds>\\d+(.\\d+)?)S)?)?$')

def parse_date(value):
    """Parses a string and return a datetime.date.

    Raises ValueError if the input is well formatted but not a valid date.
    Returns None if the input isn't well formatted.
    """
    match = date_re.match(value)
    if match:
        kw = {k:int(v) for k, v in six.iteritems(match.groupdict())}
        return datetime.date(**kw)


def parse_time(value):
    """Parses a string and return a datetime.time.

    This function doesn't support time zone offsets.

    Raises ValueError if the input is well formatted but not a valid time.
    Returns None if the input isn't well formatted, in particular if it
    contains an offset.
    """
    match = time_re.match(value)
    if match:
        kw = match.groupdict()
        if kw['microsecond']:
            kw['microsecond'] = kw['microsecond'].ljust(6, '0')
        kw = {k:int(v) for k, v in six.iteritems(kw) if v is not None if v is not None}
        return datetime.time(**kw)


def parse_datetime(value):
    """Parses a string and return a datetime.datetime.

    This function supports time zone offsets. When the input contains one,
    the output uses a timezone with a fixed offset from UTC.

    Raises ValueError if the input is well formatted but not a valid datetime.
    Returns None if the input isn't well formatted.
    """
    match = datetime_re.match(value)
    if match:
        kw = match.groupdict()
        if kw['microsecond']:
            kw['microsecond'] = kw['microsecond'].ljust(6, '0')
        tzinfo = kw.pop('tzinfo')
        if tzinfo == 'Z':
            tzinfo = utc
        elif tzinfo is not None:
            offset_mins = int(tzinfo[-2:]) if len(tzinfo) > 3 else 0
            offset = 60 * int(tzinfo[1:3]) + offset_mins
            if tzinfo[0] == '-':
                offset = -offset
            tzinfo = get_fixed_timezone(offset)
        kw = {k:int(v) for k, v in six.iteritems(kw) if v is not None if v is not None}
        kw['tzinfo'] = tzinfo
        return datetime.datetime(**kw)
    else:
        return


def parse_duration(value):
    """Parses a duration string and returns a datetime.timedelta.

    The preferred format for durations in Django is '%d %H:%M:%S.%f'.

    Also supports ISO 8601 representation.
    """
    match = standard_duration_re.match(value)
    if not match:
        match = iso8601_duration_re.match(value)
    if match:
        kw = match.groupdict()
        sign = -1 if kw.pop('sign', '+') == '-' else 1
        if kw.get('microseconds'):
            kw['microseconds'] = kw['microseconds'].ljust(6, '0')
        if kw.get('seconds') and kw.get('microseconds') and kw['seconds'].startswith('-'):
            kw['microseconds'] = '-' + kw['microseconds']
        kw = {k:float(v) for k, v in six.iteritems(kw) if v is not None if v is not None}
        return sign * datetime.timedelta(**kw)