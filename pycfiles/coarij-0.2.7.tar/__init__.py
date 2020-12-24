# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/coards/__init__.py
# Compiled at: 2013-06-04 21:21:53
__doc__ = '\nConvert COARDS time specification to a datetime object.\n\n'
from datetime import datetime, timedelta
import re, warnings
EPOCH = datetime(1970, 1, 1)
SECOND = 1.0
MINUTE = 60.0
HOUR = 3600.0
DAY = 86400.0
SHAKE = 1e-08
SIDEREAL_DAY = 86164.09
SIDEREAL_HOUR = 3590.17
SIDEREAL_MINUTE = 59.83617
SIDEREAL_SECOND = 0.9972696
SIDEREAL_YEAR = 31558150.0
TROPICAL_YEAR = 31556925.9747
LUNAR_MONTH = 29.530589 * DAY
COMMON_YEAR = 365 * DAY
LEAP_YEAR = 366 * DAY
JULIAN_YEAR = 365.25 * DAY
GREGORIAN_YEAR = 365.2425 * DAY
SIDEREAL_MONTH = 27.321661 * DAY
TROPICAL_MONTH = 27.321582 * DAY
FORTNIGHT = 14 * DAY
WEEK = 7 * DAY
JIFFY = 0.01
EON = 1000000000.0 * TROPICAL_YEAR
MONTH = TROPICAL_YEAR / 12
MILLISECOND = 0.001
MICROSECOND = 1e-06

class ParserError(Exception):
    pass


class Parser(object):

    def __init__(self, units):
        parts = units.split(' since ')
        self.units = parse_units(parts[0])
        self.offset = parse_date(parts[1])

    def __call__(self, value):
        seconds = value * self.units
        try:
            date = EPOCH + timedelta(seconds=self.offset + seconds)
        except OverflowError:
            warnings.warn('Shifted data 366 days to the future, since year zero does not exist.', UserWarning)
            date = EPOCH + timedelta(seconds=self.offset + seconds + LEAP_YEAR)

        return date


class Formatter(object):

    def __init__(self, units):
        parts = units.split(' since ')
        self.units = parse_units(parts[0])
        self.offset = parse_date(parts[1])

    def __call__(self, date):
        dt = date - EPOCH
        value = dt.days * DAY + dt.seconds + dt.microseconds * MICROSECOND - self.offset
        return value / self.units


class Converter(object):

    def __init__(self, from_, to):
        self.parser = Parser(from_)
        self.formatter = Formatter(to)

    def __call__(self, value):
        return self.formatter(self.parser(value))


def parse(value, units):
    """
    Parse a COARDS compliant date::

        >>> parse(0, "hours since 1970-01-01 00:00:00")
        datetime.datetime(1970, 1, 1, 0, 0)
        >>> parse(0, "hours since 1970-01-01 00:00:00 +2:30")
        datetime.datetime(1969, 12, 31, 21, 30)
        >>> parse(10, "hours since 1996-1-1") 
        datetime.datetime(1996, 1, 1, 10, 0)
        >>> parse(10, "hours since 1-1-1")
        datetime.datetime(1, 1, 1, 10, 0)
        >>> parse(10, "hours since 1990-11-25 12:00:00")
        datetime.datetime(1990, 11, 25, 22, 0)
        >>> parse(10, "hours since 1990-11-25 12:00")
        datetime.datetime(1990, 11, 25, 22, 0)
        >>> parse(10, "hours since 1990-11-25 12:00 +2:00")
        datetime.datetime(1990, 11, 25, 20, 0)
        >>> parse(10, "hours since 1990-11-25 12:00 UTC")
        datetime.datetime(1990, 11, 25, 22, 0)
        >>> parse(10, "seconds since 1970-1-1")
        datetime.datetime(1970, 1, 1, 0, 0, 10)

    It works with a year that never existed, since it's usual to have the
    origin set to the year zero in climatological datasets::

        >>> parse(366, "days since 0000-01-01 00:00:00")
        datetime.datetime(1, 1, 1, 0, 0)

    """
    parser = Parser(units)
    return parser(value)


def format(date, units):
    """
    Convert a datetime object into a COARDS compliant date::

        >>> print format(datetime(1970, 1, 1, 0, 0), "hours since 1970-01-01 00:00:00")
        0.0
        >>> print format(datetime(1969, 12, 31, 21, 30), "hours since 1970-01-01 00:00:00 +2:30")
        0.0
        >>> print format(datetime(1996, 1, 1, 10, 0), "hours since 1996-1-1") 
        10.0
        >>> print format(datetime(1, 1, 1, 10, 0), "hours since 1-1-1")
        10.0
        >>> print format(datetime(1990, 11, 25, 22, 0), "hours since 1990-11-25 12:00:00")
        10.0
        >>> print format(datetime(1990, 11, 25, 22, 0), "hours since 1990-11-25 12:00")
        10.0
        >>> print format(datetime(1990, 11, 25, 20, 0), "hours since 1990-11-25 12:00 +2:00")
        10.0
        >>> print format(datetime(1990, 11, 25, 22, 0), "hours since 1990-11-25 12:00 UTC")
        10.0
        >>> print format(datetime(1970, 1, 1, 0, 0, 10), "seconds since 1970-1-1")
        10.0

    It works with a year that never existed, since it's usual to have the
    origin set to the year zero in climatological datasets::

        >>> print format(datetime(1, 1, 1, 0, 0), "days since 0000-01-01 00:00:00")
        366.0

    """
    formatter = Formatter(units)
    return formatter(date)


def parse_units(units):
    """
    Parse units.

    This function transforms all Udunits defined time units, returning it
    converted to seconds::

        >>> print parse_units("min")
        60.0

    """
    udunits = [
     (
      SECOND, ['second', 'seconds', 'sec', 's', 'secs']),
     (
      MINUTE, ['minute', 'minutes', 'min']),
     (
      HOUR, ['hour', 'hours', 'hr', 'h']),
     (
      DAY, ['day', 'days', 'd']),
     (
      SHAKE, ['shake', 'shakes']),
     (
      SIDEREAL_DAY, ['sidereal_day', 'sidereal_days']),
     (
      SIDEREAL_HOUR, ['sidereal_hour', 'sidereal_hours']),
     (
      SIDEREAL_MINUTE, ['sidereal_minute', 'sidereal_minutes']),
     (
      SIDEREAL_SECOND, ['sidereal_second', 'sidereal_seconds']),
     (
      SIDEREAL_YEAR, ['sidereal_year', 'sidereal_years']),
     (
      TROPICAL_YEAR, ['tropical_year', 'tropical_years', 'year', 'years', 'yr', 'a']),
     (
      LUNAR_MONTH, ['lunar_month', 'lunar_months']),
     (
      COMMON_YEAR, ['common_year', 'common_years']),
     (
      LEAP_YEAR, ['leap_year', 'leap_years']),
     (
      JULIAN_YEAR, ['julian_year', 'julian_years']),
     (
      GREGORIAN_YEAR, ['gregorian_year', 'gregorian_years']),
     (
      SIDEREAL_MONTH, ['sidereal_month', 'sidereal_months']),
     (
      TROPICAL_MONTH, ['tropical_month', 'tropical_months']),
     (
      FORTNIGHT, ['fortnight', 'fortnights']),
     (
      WEEK, ['week', 'weeks']),
     (
      JIFFY, ['jiffy', 'jiffies']),
     (
      EON, ['eon', 'eons']),
     (
      MONTH, ['month', 'months']),
     (
      MILLISECOND, ['msec', 'msecs']),
     (
      MICROSECOND, ['usec', 'usecs', 'microsecond', 'microseconds'])]
    for seconds, valid in udunits:
        if units in valid:
            return seconds

    raise ParserError('Invalid date units: %s' % units)


def parse_date(date):
    """
    Parses a date string and returns number of seconds from the EPOCH.

    """
    p = re.compile('(?P<year>\\d{1,4})           # yyyy\n                        -                           #\n                        (?P<month>\\d{1,2})          # mm or m\n                        -                           #\n                        (?P<day>\\d{1,2})            # dd or d\n                                                    #\n                        (?:                         # [optional time and timezone]\n                            (?:\\s|T)                #\n                            (?P<hour>\\d{1,2})       #   hh or h\n                            :?                      #\n                            (?P<min>\\d{1,2})?       #   mm or m\n                            (?:                     #   [optional seconds]\n                                :                   #\n                                (?P<sec>\\d{1,2})    #       ss or s\n                                                    #\n                                (?:                 #       [optional decisecond]\n                                    \\.              #           .\n                                    (?P<dsec>\\d)    #           s\n                                )?                  #    \n                            )?                      #\n                            (?:                     #   [optional timezone]\n                                \\s?                 #\n                                ((?:                #\n                                    (?P<ho>[+-]?    #           [+ or -]\n                                    \\d{1,2})        #           hh or h\n                                    :?              #           [:]\n                                    (?P<mo>\\d{2})?  #           [mm]\n                                )                   #\n                                |                   #           or\n                                (?:UTC)|(?:Z))      #           UTC | Z\n                            )?                      #\n                        )?                          #\n                        $                           # EOL\n                    ', re.VERBOSE)
    m = p.match(date)
    if m:
        c = m.groupdict(0)
        for k, v in c.items():
            c[k] = int(v)

        tz_offset = c['ho'] * HOUR + c['mo'] * MINUTE
        if c['year'] == 0:
            c['year'] = 1
            year_offset = LEAP_YEAR
        else:
            year_offset = 0
        origin = datetime(c['year'], c['month'], c['day'], c['hour'], c['min'], c['sec'], c['dsec'] * 100000)
        dt = origin - EPOCH
        return dt.days * DAY + dt.seconds + dt.microseconds * MICROSECOND - year_offset - tz_offset
    raise ParserError('Invalid date: %s' % date)


from_udunits = parse
to_udunits = format

def _test():
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    _test()