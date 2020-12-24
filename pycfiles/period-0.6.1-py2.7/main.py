# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/period/main.py
# Compiled at: 2015-03-27 10:08:24
"""Deal with time periods

The single function in_period(time, period) determines if a given time
period string matches the time given.  The syntax is based loosely on
the class specifications used in Cfengine (http://www.iu.hioslo.no/cfengine).
"""
from __future__ import print_function
from builtins import range
from builtins import object
import string, re, time, os
WEEK_MAP = [
 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday',
 'Friday', 'Saturday']
MONTH_MAP = ['January', 'February', 'March', 'April', 'May', 'June',
 'July', 'August', 'September', 'October', 'November', 'December']
DAYTYPE_MAP = ['Weekday', 'Weekend']

def _remove_otiose(lst):
    """lift deeply nested expressions out of redundant parentheses"""
    listtype = type([])
    while type(lst) == listtype and len(lst) == 1:
        lst = lst[0]

    return lst


class PeriodParser(object):
    """Parse time period specifications."""

    def __init__(self):
        self.SPECIAL = '().|!'

    def parse(self, str=None):
        if str:
            self.str = str
            self.i = 0
            self.len = len(str)
            self.level = 0
        expr = []
        tok = self.get_token()
        while tok != '':
            if tok == ')':
                self.level = self.level - 1
                if self.level < 0:
                    break
                else:
                    return expr
            elif tok == '(':
                self.level = self.level + 1
                sexpr = _remove_otiose(self.parse())
                expr.append(sexpr)
            else:
                expr.append(tok)
            tok = self.get_token()

        if self.level == 0:
            return expr
        if self.level > 0:
            raise Exception('mismatched opening parenthesis in expression')
        else:
            raise Exception('mismatched closing parenthesis in expression')

    def get_token(self):
        if self.i >= self.len:
            return ''
        else:
            if self.str[self.i] in self.SPECIAL:
                self.i = self.i + 1
                return self.str[(self.i - 1)]
            tok = ''
            while self.i < self.len - 1:
                if self.str[self.i] in self.SPECIAL:
                    break
                else:
                    tok = tok + self.str[self.i]
                    self.i = self.i + 1

            if self.str[self.i] not in self.SPECIAL:
                tok = tok + self.str[self.i]
                self.i = self.i + 1
            return tok


class Stack(object):

    def __init__(self):
        self.s = []

    def push(self, datum):
        self.s.append(datum)

    def pop(self):
        return self.s.pop()

    def empty(self):
        return len(self.s) == 0

    def __repr__(self):
        return repr(self.s)


_precedence = {'.': 10, '|': 5, 
   '!': 30}

class PeriodSyntax(object):

    def __init__(self):
        self.ops = [
         '.', '|', '!']
        self.uops = ['!']

    def flatten(self, lst=None):
        """syntax.flatten(token_stream) - compile period tokens

        This turns a stream of tokens into p-code for the trivial
        stack machine that evaluates period expressions in in_period.
        """
        tree = []
        uops = []
        s = Stack()
        group_len = 0
        for item in lst:
            if type(item) == type([]):
                tree = tree + self.flatten(item)
                group_len = group_len + 1
                for uop in uops:
                    tree.append(uop)

                uops = []
            elif item in self.ops and item not in self.uops:
                if not s.empty():
                    prev_op = s.pop()
                    if _precedence[prev_op] > _precedence[item]:
                        s.push(prev_op)
                        for i in range(group_len - 1):
                            tree.append(s.pop())

                        group_len = 0
                    else:
                        s.push(prev_op)
                    s.push(item)
                else:
                    s.push(item)
            elif item in self.uops:
                uops.append(item)
            else:
                tree.append(item)
                group_len = group_len + 1
                for uop in uops:
                    tree.append(uop)

                uops = []

        while not s.empty():
            tree.append(s.pop())

        for uop in uops:
            tree.append(uop)

        return tree


class _Time(object):
    """Utility class for symbolic date manipulation."""

    def __init__(self, tyme=None):
        if not tyme:
            self.time = time.localtime(time.time())
        else:
            self.time = time.localtime(tyme)
        self._set_props()

    def _set_props(self):
        self.weekday, self.month, self.day, self.hr, self.minute, self.week, self.year = str.split(time.strftime('%A %B %d %H %M %U %Y', self.time))
        if self.weekday in ('Saturday', 'Sunday'):
            self.daytype = 'Weekend'
        else:
            self.daytype = 'Weekday'


_parser = PeriodParser()
_syntax = PeriodSyntax()

def in_period(period, tyme=None):
    now = _Time(tyme)
    periodcode = _syntax.flatten(_parser.parse(period))
    s = Stack()
    try:
        for item in periodcode:
            if item == '.':
                a = s.pop()
                b = s.pop()
                s.push(a and b)
            elif item == '|':
                a = s.pop()
                b = s.pop()
                s.push(a or b)
            elif item == '!':
                s.push(not s.pop())
            else:
                s.push(_check_timespec(item, now))

        return s.pop()
    except IndexError:
        raise Exception('bad period (too many . or | operators?): %s' % period)


def _check_timespec(timespec, now):
    if timespec[0:2] == 'Yr':
        return now.year in _parse_Yr(timespec)
    if timespec[0:2] == 'Hr':
        return now.hr in _parse_Hr(timespec)
    if timespec[0:3] == 'Min':
        return now.minute in _parse_Min(timespec)
    if timespec[0:3] == 'Day':
        return now.day in _parse_Day(timespec)
    if timespec in WEEK_MAP:
        return now.weekday == timespec
    if timespec[0:4] == 'Week':
        if timespec in DAYTYPE_MAP:
            return now.daytype == timespec
        else:
            return now.week in _parse_Week(timespec)

    else:
        if timespec in MONTH_MAP:
            return now.month == timespec
        if timespec == 'Always':
            return 1
        if timespec == 'Never':
            return 0
        if '-' in timespec:
            first = timespec[0:str.index(timespec, '-')]
            if first in MONTH_MAP:
                return now.month in _compose_symbolic_range('month', timespec)
            if first in WEEK_MAP:
                return now.weekday in _compose_symbolic_range('weekday', timespec)
            raise Exception('Bad range specification: %s' % timespec)
        else:
            raise Exception('Bad time specification: %s' % timespec)


def _parse_Yr(year):
    """Return a hash of the matching years, coping with ranges."""
    return _compose_range('Yr', year, fill=4)


def _parse_Hr(hour):
    """Return a hash of the matching hours, coping with ranges."""
    return _compose_range('Hr', hour, fill=2)


def _parse_Min(min):
    """Return a hash of the matching days, coping with ranges."""
    return _compose_range('Min', min, fill=2)


def _parse_Day(day):
    """Return a hash of the matching days, coping with ranges."""
    return _compose_range('Day', day, fill=2)


def _parse_Week(week):
    """Return a hash of the matching weeks, coping with ranges."""
    return _compose_range('Week', week, fill=2)


def _compose_range(pattern, rule, fill=2):
    """oc._compose_range('Week', 'Week04-Week09', fill=2) - hash a range.

    This takes apart a range of times and returns a dictionary of
    all intervening values appropriately set.  The fill value is
    used to format the time numbers.
    """
    keys = []
    mask = len(pattern)
    for rule in str.split(rule, ','):
        if '-' not in rule:
            if rule[:mask] == pattern:
                keys.append(rule[mask:])
            else:
                keys.append(rule)
        else:
            start, end = str.split(rule, '-')
            if rule[:mask] == pattern:
                start = int(start[mask:])
            else:
                start = int(start)
            if end[0:mask] == pattern:
                end = int(end[mask:])
            else:
                end = int(end)
            key = '%%0%ii' % fill
            for i in range(start, end + 1):
                keys.append(key % i)

    return keys


def _compose_symbolic_range(pattern, rule):
    if pattern == 'weekday':
        cycle = WEEK_MAP
    else:
        if pattern == 'month':
            cycle = MONTH_MAP
        else:
            raise Exception('Unknown cycle name: %s' % pattern)
        clen = len(cycle)
        keys = []
        for rule in str.split(rule, ','):
            if '-' not in rule:
                keys.append(rule)
            else:
                start, end = str.split(rule, '-')
                if not (start in cycle and end in cycle):
                    raise Exception('Unknown %s name: %s' % (pattern, rule))
                start_i = cycle.index(start)
                while cycle[start_i] != end:
                    keys.append(cycle[start_i])
                    start_i = (start_i + 1) % clen

                keys.append(cycle[start_i])

    return keys


def is_holiday(now=None, holidays='/etc/acct/holidays'):
    """is_holiday({now}, {holidays="/etc/acct/holidays"}"""
    now = _Time(now)
    if not os.path.exists(holidays):
        raise Exception('There is no holidays file: %s' % holidays)
    f = open(holidays, 'r')
    line = f.readline()
    while line[0] == '*':
        line = f.readline()

    year, primestart, primeend = str.split(line)
    if not year == now.year:
        return 0
    while line != '':
        if line[0] == '*':
            line = f.readline()
            continue
        try:
            month, day = str.split(str.split(line)[0], '/')
            if len(day) == 1:
                day = '0' + day
            month = MONTH_MAP[(int(month) - 1)]
            if month == now.month and day == now.day:
                return 1
            line = f.readline()
        except:
            line = f.readline()
            continue

    return 0


if __name__ == '__main__':
    for a in ['Friday', 'Friday.January', 'Friday.January.Day04', 'Friday.January.Day05',
     'Friday.January.Day02-12',
     'Friday.January.!Day02-12',
     'April.Yr1988-2001',
     '(January|April).Yr1988-2002',
     'May.Hr05-12',
     'Tuesday.Hr07-23',
     'January.Hr05-09,11-21',
     'Week00', 'Week02',
     '!Week00', '!Week02',
     'Hr12|Hr13|Hr14|Hr15', '(Hr12|Hr13|Hr14|Hr15)',
     'Weekday', 'Weekend',
     'Weekday.Min50-55',
     'Weekday.Min05-50',
     'Weekday.Hr07-23',
     'Monday-Friday',
     'December-February',
     'January-March.Monday-Friday',
     '!January-March.Monday-Friday',
     'January-March.!Weekend',
     '(Monday|Friday).Hr09-17',
     '!!!Weekday',
     '!!!!Weekday',
     '((((Yr2002))))',
     'Friday-Flopday',
     'Monday||Tuesday',
     '(Monday|Tuesday',
     'Monday|Tuesday)',
     '(Monday|Friday)).Hr09-17',
     '(Monday|!(Weekday)).Hr11-14',
     '(Monday|(Weekday)).Hr11-14',
     '(Monday|(Friday.December-March)).Yr2002']:
        try:
            print('*', a, in_period(a))
        except Exception as e:
            print('ERR', e)

    if os.path.exists('holidays'):
        print('*', 'holiday', is_holiday(holidays='holidays'))