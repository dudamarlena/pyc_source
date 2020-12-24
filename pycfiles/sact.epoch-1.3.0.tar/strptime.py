# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vaab/lib/python/site-packages/sact/epoch/strptime.py
# Compiled at: 2015-01-20 01:48:13
"""
.. :doctest:

"""
import time, _strptime
from datetime import date as datetime_date

def first(l, predicate):
    for e in l:
        if predicate(e):
            return e

    raise ValueError('No element in list matches given predicate.')


def strptime(data_string, format='%a %b %d %H:%M:%S %Y', reference=(1900, 1, 1, 0, 0, 0, -1, -1, -1), complete_with_zeroes=True):
    """Return time struct and microseconds based on an input and format string

    An optional ``reference`` is set by default to 1900-01-01 00:00:00.

    ``reference`` field is a tuple with:

    (year, month, day, hour, minute, second, weekday, julian, tz), microseconds

    Please note that weekday and julian will be ignored.

        >>> from sact.epoch.strptime import strptime
        >>> strptime('13:05', '%H:%M',
        ...          reference=((2000, 1, 1, 0, 0, 30, -1, -1, -1), 5))
        (time.struct_time(tm_year=2000, tm_mon=1, tm_mday=1, tm_hour=13, tm_min=5, tm_sec=0, tm_wday=5, tm_yday=1, tm_isdst=-1), 0)

    Notice how all the left most values (the biggest weight value)
    where used from the given reference, and how the left most value
    (least weight values) was zeroed. The middle part is what was
    parsed.

    You can switch of the zeroing of the left most part:

        >>> strptime('13:05', '%H:%M',
        ...          reference=((2000, 1, 1, 0, 0, 0, -1, -1, -1), 5),
        ...          complete_with_zeroes=False)
        (time.struct_time(tm_year=2000, tm_mon=1, tm_mday=1, tm_hour=13, tm_min=5, tm_sec=0, tm_wday=5, tm_yday=1, tm_isdst=-1), 5)

    """
    with _strptime._cache_lock:
        if _strptime._getlang() != _strptime._TimeRE_cache.locale_time.lang:
            _strptime._TimeRE_cache = TimeRE()
            _strptime._regex_cache.clear()
        if len(_strptime._regex_cache) > _strptime._CACHE_MAX_SIZE:
            _strptime._regex_cache.clear()
        locale_time = _strptime._TimeRE_cache.locale_time
        format_regex = _strptime._regex_cache.get(format)
        if not format_regex:
            try:
                format_regex = _strptime._TimeRE_cache.compile(format)
            except KeyError as err:
                bad_directive = err.args[0]
                if bad_directive == '\\':
                    bad_directive = '%'
                del err
                raise ValueError("'%s' is a bad directive in format '%s'" % (
                 bad_directive, format))
            except IndexError:
                raise ValueError("stray %% in format '%s'" % format)

            _strptime._regex_cache[format] = format_regex
    found = format_regex.match(data_string)
    if not found:
        raise ValueError('time data %r does not match format %r' % (
         data_string, format))
    if len(data_string) != found.end():
        raise ValueError('unconverted data remains: %s' % data_string[found.end():])
    (year, month, day, hour, minute, second, weekday, julian, tz), fraction = reference
    julian = -1
    weekday = -1
    week_of_year = -1
    week_of_year_start = -1
    found_dict = found.groupdict()
    for group_key in found_dict.keys():
        if group_key == 'y':
            year = int(found_dict['y'])
            if year <= 68:
                year += 2000
            else:
                year += 1900
        elif group_key == 'Y':
            year = int(found_dict['Y'])
        elif group_key == 'm':
            month = int(found_dict['m'])
        elif group_key == 'B':
            month = locale_time.f_month.index(found_dict['B'].lower())
        elif group_key == 'b':
            month = locale_time.a_month.index(found_dict['b'].lower())
        elif group_key == 'd':
            day = int(found_dict['d'])
        elif group_key == 'H':
            hour = int(found_dict['H'])
        elif group_key == 'I':
            hour = int(found_dict['I'])
            ampm = found_dict.get('p', '').lower()
            if ampm in ('', locale_time.am_pm[0]):
                if hour == 12:
                    hour = 0
            elif ampm == locale_time.am_pm[1]:
                if hour != 12:
                    hour += 12
        elif group_key == 'M':
            minute = int(found_dict['M'])
        elif group_key == 'S':
            second = int(found_dict['S'])
        elif group_key == 'f':
            s = found_dict['f']
            s += '0' * (6 - len(s))
            fraction = int(s)
        elif group_key == 'A':
            weekday = locale_time.f_weekday.index(found_dict['A'].lower())
        elif group_key == 'a':
            weekday = locale_time.a_weekday.index(found_dict['a'].lower())
        elif group_key == 'w':
            weekday = int(found_dict['w'])
            if weekday == 0:
                weekday = 6
            else:
                weekday -= 1
        elif group_key == 'j':
            julian = int(found_dict['j'])
        elif group_key in ('U', 'W'):
            week_of_year = int(found_dict[group_key])
            if group_key == 'U':
                week_of_year_start = 6
            else:
                week_of_year_start = 0
        elif group_key == 'Z':
            found_zone = found_dict['Z'].lower()
            for value, tz_values in enumerate(locale_time.timezone):
                if found_zone in tz_values:
                    if time.tzname[0] == time.tzname[1] and time.daylight and found_zone not in ('utc',
                                                                                                 'gmt'):
                        break
                    else:
                        tz = value
                        break

    if julian == -1 and week_of_year != -1 and weekday != -1:
        week_starts_Mon = True if week_of_year_start == 0 else False
        julian = _strptime._calc_julian_from_U_or_W(year, week_of_year, weekday, week_starts_Mon)
    if complete_with_zeroes:
        idxs = ('j', 'Y', 'mBb', 'UW', 'dAaw', 'HI', 'M', 'S', 'f')
        specified = [ idxs.index(gk) for gk in [ first(idxs, lambda key_group: k in key_group)
         for k in found_dict.keys()
                                               ]
                    ]
        rightmost_specified = max(specified) if len(specified) else 0
        base = (1900, 1, 1, 1, 0, 0, 0, 0)
        values = (year, month, week_of_year, day, hour, minute, second, fraction)
        year, month, week_of_year, day, hour, minute, second, fraction = values[:rightmost_specified] + base[rightmost_specified:]
    if julian == -1:
        julian = datetime_date(year, month, day).toordinal() - datetime_date(year, 1, 1).toordinal() + 1
    else:
        datetime_result = datetime_date.fromordinal(julian - 1 + datetime_date(year, 1, 1).toordinal())
        year = datetime_result.year
        month = datetime_result.month
        day = datetime_result.day
    if weekday == -1:
        weekday = datetime_date(year, month, day).weekday()
    return (
     time.struct_time((year, month, day,
      hour, minute, second,
      weekday, julian, tz)), fraction)