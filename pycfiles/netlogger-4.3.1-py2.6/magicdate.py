# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/magicdate.py
# Compiled at: 2009-12-08 17:43:30
import re, datetime, calendar
from optparse import Option, OptionValueError
from copy import copy

def check_magicdate(option, opt, value):
    try:
        return magicdate(value)
    except:
        raise OptionValueError('option %s: invalid date value: %r' % (opt, value))


class MagicDateOption(Option):
    TYPES = Option.TYPES + ('magicdate', )
    TYPE_CHECKER = copy(Option.TYPE_CHECKER)
    TYPE_CHECKER['magicdate'] = check_magicdate


res = [
 (
  re.compile('^\n                ((?P<weeks>\\d+) \\s weeks?)?\n                [^\\d]*\n                ((?P<days>\\d+) \\s days?)?\n                [^\\d]*\n                ((?P<hours>\\d+) \\s hours?)?\n                [^\\d]*\n                ((?P<minutes>\\d+) \\s minutes?)?\n                [^\\d]*\n                ((?P<seconds>\\d+) \\s seconds?)?\n                \\s\n                ago\n            ', re.VERBOSE | re.IGNORECASE),
  lambda m: datetime.datetime.today() - datetime.timedelta(days=int(m.group('days') or 0), seconds=int(m.group('seconds') or 0), minutes=int(m.group('minutes') or 0), hours=int(m.group('hours') or 0), weeks=int(m.group('weeks') or 0))),
 (
  re.compile('^\n                tod                             # Today\n            ', re.VERBOSE | re.IGNORECASE),
  lambda m: datetime.date.today()),
 (
  re.compile('^\n                now                             # Now\n            ', re.VERBOSE | re.IGNORECASE),
  lambda m: datetime.datetime.now()),
 (
  re.compile('^\n                tom                             # Tomorrow\n            ', re.VERBOSE | re.IGNORECASE),
  lambda m: datetime.date.today() + datetime.timedelta(days=1)),
 (
  re.compile('^\n                yes                             # Yesterday\n            ', re.VERBOSE | re.IGNORECASE),
  lambda m: datetime.date.today() - datetime.timedelta(days=1)),
 (
  re.compile('^\n                (?P<day>\\d{1,2})                # 4\n                (?:st|nd|rd|th)?                # optional suffix\n                $                               # EOL\n            ', re.VERBOSE | re.IGNORECASE),
  lambda m: datetime.date.today().replace(day=int(m.group('day')))),
 (
  re.compile('^\n                (?P<day>\\d{1,2})                # 4\n                (?:st|nd|rd|th)?                # optional suffix\n                \\s+                             # whitespace\n                (?P<month>\\w+)                  # Jan\n                $                               # EOL\n            ', re.VERBOSE | re.IGNORECASE),
  lambda m: datetime.date.today().replace(day=int(m.group('day')), month=_parseMonth(m.group('month')))),
 (
  re.compile('^\n                (?P<day>\\d{1,2})                # 4\n                (?:st|nd|rd|th)?                # optional suffix\n                \\s+                             # whitespace\n                (?P<month>\\w+)                  # Jan\n                ,?                              # optional comma\n                \\s+                             # whitespace\n                (?P<year>\\d{4})                 # 2003\n                $                               # EOL\n            ', re.VERBOSE | re.IGNORECASE),
  lambda m: datetime.date(year=int(m.group('year')), month=_parseMonth(m.group('month')), day=int(m.group('day')))),
 (
  re.compile('^\n                (?P<month>\\w+)                  # Jan\n                \\s+                             # whitespace\n                (?P<day>\\d{1,2})                # 4\n                (?:st|nd|rd|th)?                # optional suffix\n                $                               # EOL\n            ', re.VERBOSE | re.IGNORECASE),
  lambda m: datetime.date.today().replace(day=int(m.group('day')), month=_parseMonth(m.group('month')))),
 (
  re.compile('^\n                (?P<month>\\w+)                  # Jan\n                \\s+                             # whitespace\n                (?P<day>\\d{1,2})                # 4\n                (?:st|nd|rd|th)?                # optional suffix\n                ,?                              # optional comma\n                \\s+                             # whitespace\n                (?P<year>\\d{4})                 # 2003\n                $                               # EOL\n            ', re.VERBOSE | re.IGNORECASE),
  lambda m: datetime.date(year=int(m.group('year')), month=_parseMonth(m.group('month')), day=int(m.group('day')))),
 (
  re.compile('^\n                (?P<month>0?[1-9]|10|11|12)     # m or mm\n                /                               #\n                (?P<day>0?[1-9]|[12]\\d|30|31)   # d or dd\n                /                               #\n                (?P<year>\\d{4})                 # yyyy\n                $                               # EOL\n            ', re.VERBOSE | re.IGNORECASE),
  lambda m: datetime.date(year=int(m.group('year')), month=int(m.group('month')), day=int(m.group('day')))),
 (
  re.compile('^\n                (?P<day>0?[1-9]|[12]\\d|30|31)   # d or dd\n                /                               #\n                (?P<month>0?[1-9]|10|11|12)     # m or mm\n                /                               #\n                (?P<year>\\d{4})                 # yyyy\n                $                               # EOL\n            ', re.VERBOSE | re.IGNORECASE),
  lambda m: datetime.date(year=int(m.group('year')), month=int(m.group('month')), day=int(m.group('day')))),
 (
  re.compile('^\n                (?P<year>\\d{4})                 # yyyy\n                -                               #\n                (?P<month>0?[1-9]|10|11|12)     # m or mm\n                -                               #\n                (?P<day>0?[1-9]|[12]\\d|30|31)   # d or dd\n                $                               # EOL\n            ', re.VERBOSE | re.IGNORECASE),
  lambda m: datetime.date(year=int(m.group('year')), month=int(m.group('month')), day=int(m.group('day')))),
 (
  re.compile('^\n                (?P<year>\\d{4})                 # yyyy\n                (?P<month>0?[1-9]|10|11|12)     # m or mm\n                (?P<day>0?[1-9]|[12]\\d|30|31)   # d or dd\n                $                               # EOL\n            ', re.VERBOSE | re.IGNORECASE),
  lambda m: datetime.date(year=int(m.group('year')), month=int(m.group('month')), day=int(m.group('day')))),
 (
  re.compile('^\n                next                            # next\n                \\s+                             # whitespace\n                (?P<weekday>\\w+)                # Tuesday\n                $                               # EOL\n            ', re.VERBOSE | re.IGNORECASE),
  lambda m: _nextWeekday(_parseWeekday(m.group('weekday')))),
 (
  re.compile('^\n                (last                           # last\n                \\s+)?                           # whitespace\n                (?P<weekday>\\w+)                # Tuesday\n                $                               # EOL\n            ', re.VERBOSE | re.IGNORECASE),
  lambda m: _lastWeekday(_parseWeekday(m.group('weekday'))))]

def _parseMonth(input):
    months = ('January February March April May June July August September October November December').split(' ')
    for (i, month) in enumerate(months):
        p = re.compile(input, re.IGNORECASE)
        if p.match(month):
            return i + 1
    else:
        raise Exception


def _parseWeekday(input):
    days = ('Monday Tuesday Wednesday Thursday Friday Saturday Sunday').split(' ')
    for (i, day) in enumerate(days):
        p = re.compile(input, re.IGNORECASE)
        if p.match(day):
            return i
    else:
        raise Exception


def _nextWeekday(weekday):
    day = datetime.date.today() + datetime.timedelta(days=1)
    while calendar.weekday(*day.timetuple()[:3]) != weekday:
        day = day + datetime.timedelta(days=1)

    return day


def _lastWeekday(weekday):
    day = datetime.date.today() - datetime.timedelta(days=1)
    while calendar.weekday(*day.timetuple()[:3]) != weekday:
        day = day - datetime.timedelta(days=1)

    return day


def magicdate(input):
    for (r, f) in res:
        m = r.match(input.strip())
        if m:
            return f(m)