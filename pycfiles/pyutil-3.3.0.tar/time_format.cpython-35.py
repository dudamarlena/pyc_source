# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/code/pyutil/pyutil/time_format.py
# Compiled at: 2019-06-26 11:58:00
# Size of source mod 2**32: 2370 bytes
import calendar, datetime, re, time

def iso_utc_date(now=None, t=time.time):
    if now is None:
        now = t()
    return datetime.datetime.utcfromtimestamp(now).isoformat()[:10]


def iso_utc(now=None, sep=' ', t=time.time, suffix='Z'):
    if now is None:
        now = t()
    return datetime.datetime.utcfromtimestamp(now).isoformat(sep) + suffix


def iso_local(now=None, sep=' ', t=time.time):
    if now is None:
        now = t()
    return datetime.datetime.fromtimestamp(now).isoformat(sep)


def iso_utc_time_to_seconds(isotime, _conversion_re=re.compile('(?P<year>\\d{4})-(?P<month>\\d{2})-(?P<day>\\d{2})[T_ ](?P<hour>\\d{2}):(?P<minute>\\d{2}):(?P<second>\\d{2})(?P<subsecond>\\.\\d+)?Z?')):
    """
    The inverse of iso_utc().

    Real ISO-8601 is "2003-01-08T06:30:59Z".  We also accept
    "2003-01-08 06:30:59Z" as suggested by RFC 3339.  We also accept
    "2003-01-08_06:30:59Z".  We also accept the trailing 'Z' to be omitted.
    """
    m = _conversion_re.match(isotime)
    if not m:
        raise ValueError(isotime, 'not a complete ISO8601 timestamp')
    year, month, day = int(m.group('year')), int(m.group('month')), int(m.group('day'))
    hour, minute, second = int(m.group('hour')), int(m.group('minute')), int(m.group('second'))
    subsecstr = m.group('subsecond')
    if subsecstr:
        subsecfloat = float(subsecstr)
    else:
        subsecfloat = 0
    return calendar.timegm((year, month, day, hour, minute, second, 0, 1, 0)) + subsecfloat


def parse_duration(s):
    orig = s
    unit = None
    DAY = 86400
    MONTH = 31 * DAY
    YEAR = 365 * DAY
    if s.endswith('s'):
        s = s[:-1]
    if s.endswith('day'):
        unit = DAY
        s = s[:-len('day')]
    else:
        if s.endswith('month'):
            unit = MONTH
            s = s[:-len('month')]
        else:
            if s.endswith('mo'):
                unit = MONTH
                s = s[:-len('mo')]
            else:
                if s.endswith('year'):
                    unit = YEAR
                    s = s[:-len('YEAR')]
                else:
                    raise ValueError("no unit (like day, month, or year) in '%s'" % orig)
    s = s.strip()
    return int(s) * unit


def parse_date(s):
    return int(iso_utc_time_to_seconds(s + 'T00:00:00'))