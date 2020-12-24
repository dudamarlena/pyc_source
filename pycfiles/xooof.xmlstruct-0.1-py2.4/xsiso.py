# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xooof/xmlstruct/xsiso.py
# Compiled at: 2008-10-01 11:16:13
from mx.DateTime.ISO import *
from translations import _
import datetime

def ParseDateTimeTZ(isostring, parse_isodatetime=isodatetimeRE.match, strip=string.strip, atoi=string.atoi, atof=string.atof):
    s = strip(isostring)
    date = parse_isodatetime(s)
    if not date:
        raise ValueError, _('wrong format, use YYYY-MM-DD HH:MM:SS')
    (year, month, day, hour, minute, second, zone) = date.groups()
    year = atoi(year)
    if month is None:
        month = 1
    else:
        month = atoi(month)
    if day is None:
        day = 1
    else:
        day = atoi(day)
    if hour is None:
        hour = 0
    else:
        hour = atoi(hour)
    if minute is None:
        minute = 0
    else:
        minute = atoi(minute)
    if second is None:
        second = 0.0
    else:
        second = atof(second)
    offset = Timezone.utc_offset(zone)
    return (DateTime.DateTime(year, month, day, hour, minute, second), offset)


def ParseTimeTZ(isostring, parse_isotime=isotimeRE.match, strip=string.strip, atoi=string.atoi, atof=string.atof):
    s = strip(isostring)
    time = parse_isotime(s)
    if not time:
        raise ValueError, _('wrong format, use HH:MM:SS')
    (hour, minute, second, zone) = time.groups()
    hour = atoi(hour)
    minute = atoi(minute)
    if second is not None:
        second = atof(second)
    else:
        second = 0.0
    offset = Timezone.utc_offset(zone)
    return (DateTime.TimeDelta(hour, minute, second), offset)


date_parser = re.compile('^\n    (?P<year>\\d{4,4})\n    (?:\n        -\n        (?P<month>\\d{1,2})\n        (?:\n            -\n            (?P<day>\\d{1,2})\n            (?:\n                T\n                (?P<hour>\\d{1,2})\n                :\n                (?P<minute>\\d{1,2})\n                (?:\n                    :\n                    (?P<second>\\d{1,2})\n                    (?:\n                        \\.\n                        (?P<dec_second>\\d+)?\n                    )?\n                )?\n                (?:\n                    Z\n                    |\n                    (?:\n                        (?P<tz_sign>[+-])\n                        (?P<tz_hour>\\d{1,2})\n                        :\n                        (?P<tz_min>\\d{2,2})\n                    )\n                )?\n            )?\n        )?\n    )?\n$', re.VERBOSE)
time_parser = re.compile('^\n                (?P<hour>\\d{1,2})\n                :\n                (?P<minute>\\d{1,2})\n                (?:\n                    :\n                    (?P<second>\\d{1,2})\n                    (?:\n                        \\.\n                        (?P<dec_second>\\d+)?\n                    )?\n                )?\n                (?:\n                    Z\n                    |\n                    (?:\n                        (?P<tz_sign>[+-])\n                        (?P<tz_hour>\\d{1,2})\n                        :\n                        (?P<tz_min>\\d{2,2})\n                    )\n                )?\n$', re.VERBOSE)

def parseDateTime(isostring):
    """ parse a string and return a datetime object. """
    assert isinstance(isostring, basestring)
    r = date_parser.search(isostring)
    try:
        a = r.groupdict('0')
    except:
        raise ValueError, _('wrong format, use YYYY-MM-DD HH:MM:SS')

    dt = datetime.datetime(int(a['year']), int(a['month']) or 1, int(a['day']) or 1, int(a['hour']), int(a['minute']), int(a['second']))
    tz_hours_offset = int(a['tz_hour'])
    tz_mins_offset = int(a['tz_min'])
    if a.get('tz_sign', '+') == '-':
        return dt + datetime.timedelta(hours=tz_hours_offset, minutes=tz_mins_offset)
    else:
        return dt - datetime.timedelta(hours=tz_hours_offset, minutes=tz_mins_offset)


def parseTime(isostring):
    """ parse a string and return a time object. """
    assert isinstance(isostring, basestring)
    r = time_parser.search(isostring)
    try:
        a = r.groupdict('0')
    except:
        raise ValueError, _('wrong format, use HH:MM:SS')

    dt = datetime.datetime(1900, 1, 1, int(a['hour']), int(a['minute']), int(a['second']))
    tz_hours_offset = int(a['tz_hour'])
    tz_mins_offset = int(a['tz_min'])
    if a.get('tz_sign', '+') == '-':
        return (dt + time.timedelta(hours=tz_hours_offset, minutes=tz_mins_offset)).time()
    else:
        return (dt - datetime.timedelta(hours=tz_hours_offset, minutes=tz_mins_offset)).time()