# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/ZScheduler/utils.py
# Compiled at: 2015-07-18 19:40:58
import re
from DateTime import DateTime
from DateTime.DateTime import _MONTH_LEN
valid_char_number = re.compile('^\\d+$')
valid_char_list = re.compile('^\\d+(-\\d+)*(/\\d+)*$')
numbers = re.compile('(\\d+)')

def parse_spec(specification, min, max):
    """
    crontab spec parser/validater
    """
    specification.replace(' ', '')
    if specification == '*':
        return 1
    for element in specification.split(','):
        if not valid_char_number.match(element):
            if not valid_char_list.match(element):
                return 0
            begin, end = element.split('-')
            if end.find('/') != -1:
                end, increment = end.split('/')
                if not valid_char_number.match(increment):
                    return 0
            if not valid_char_number.match(begin) and not valid_char_number.match(end):
                return 0
        elif int(element) < min or int(element) > max:
            return 0

    return 1


def expand_spec(specification):
    """
    take  a-b/c and produce a comma-separated list of expanded numbers
    this is a prereq for plone4cron
    """
    specification = specification.replace(' ', '')
    if specification.find(',') != -1:
        parts = specification.split(',')
        return (',').join(map(lambda x: expand_spec(x), parts))
    mod = 0
    if specification.find('/') != -1:
        specification, mod = specification.split('/')
        mod = int(mod)
    if specification.find('-') != -1:
        smin, smax = specification.split('-')
        smin = int(smin)
        smax = int(smax)
        values = range(smin, smax + 1)
    else:
        values = [
         specification]
    if mod:
        tmp = [
         smin]
        while smin < smax:
            smin += mod
            if smin <= smax:
                tmp.append(smin)

        values = tmp
    return (',').join(map(lambda x: str(x), values))


def get_first_time_for_spec(specification, min):
    """
    return the first valid number from the spec
    """
    if specification == '*':
        return min
    match = numbers.search(specification)
    return match.group(0)


def get_time_for_spec(specification, value, min, max):
    """
    specification is a crontab range, value is what you currently have, min
    and max are the boundaries to this time component

    returns a tuple of the next valid value and a flag indicating if
    it had to wrap to discover this - an indication to increment the next
    time component ;)
    """
    if specification == '*':
        expansion = range(min, max + 1)
    else:
        expansion = []
        for element in specification.split(','):
            if valid_char_number.match(element):
                expansion.append(int(element))
            else:
                begin, end = element.split('-')
                begin = int(begin)
                if end.find('/') != -1:
                    end, increment = end.split('/')
                    end = int(end)
                    increment = int(increment)
                    index = begin
                    while index <= end:
                        expansion.append(index)
                        index += increment

                else:
                    end = int(end)
                    expansion.extend(range(begin, end + 1))

        expansion.sort()
        for element in expansion:
            if element >= value:
                return (element, 0)

    return (
     expansion[0], 1)


def next_day(tm, tz):
    """
    returns the beginning of the next day, allowing for month/year rollover
    """
    m = tm.month()
    y = tm.year()
    month_len = _MONTH_LEN[(y % 4 == 0 and (y % 100 != 0 or y % 400 == 0))][m]
    d = tm.day()
    if d < month_len:
        return DateTime('%s/%s/%0.2i 00:00 %s' % (y, tm.mm(), d + 1, tz))
    else:
        return next_month(tm, tz)


def next_month(tm, tz):
    """
    returns the beginning of the next month, allowing for year rollover
    """
    month = tm.month()
    if month == 12:
        return DateTime('%i/01/01 00:00 %s' % (tm.year() + 1, tz))
    else:
        return DateTime('%s/%0.2i/01 00:00 %s' % (tm.year(), month + 1, tz))