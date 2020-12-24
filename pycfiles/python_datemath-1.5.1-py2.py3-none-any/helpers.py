# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nmaccarthy/dev/misc/python-datemath/datemath/helpers.py
# Compiled at: 2020-03-25 08:44:07
"""
A basic utility module for parsing math like strings relating to dates

This is inspired by Date Math features in elasticsearch and aims to replicate the same functionality for python.

DateMath (datemath or dm) suppor addition, subtraction and rounding at various granularities of "units" (a map of units to their shorthand is below for reference).
Expressions can be chanied together and are read left to right.  '+' and '-' denote addition and subtraction while '/' denotes 'round', in this case is a 'round down' or floor.
Round requires a unit (/d), while addition and subtraction require an integer value and a unit (+1d).  Whitespace is not allowed in the expression.  Absolute datetimes with datemath 
can be made as well, with the datetime and datemath expressions delinated by '||' - example '2015-01-01||+1d' == '2015-01-02'

Maps:

y or Y      =   'year'
M           =   'month'
m           =   'minute'
d or D      =   'day'
w           =   'week'
h or H      =   'hour'
s or S      =   'second'

Examples:

Assuming our datetime is currently: '2016-01-01T00:00:00-00:00'

Expression:                 Result:
now-1h                      2015-12-31T23:00:00+00:00
now-1y                      2015-01-01T00:00:00+00:00
now+1y+2d                   2017-01-03T00:00:00+00:00
now+12h                     2016-01-01T12:00:00+00:00
now+1d/d                    2016-01-03T00:00:00+00:00
+2h                         2016-01-01T02:00:00+00:00
+1h/h                       2016-01-01T02:00:00+00:00
now+1w/w                    2016-01-11T00:00:00+00:00
now/d+7d+12h                2016-01-08T12:00:00+00:00
2016-01-01||+1d             2016-01-02T00:00:00+00:00
2015-01-01||+2w             2015-01-15T00:00:00+00:00

"""
import arrow, re, os
from dateutil import tz
import sys
debug = True if os.environ.get('DEBUG') == 'true' else False

class DateMathException(Exception):
    pass


def unitMap(c):
    """ 
        maps our units ( 'd', 'y', 'M', etc ) to shorthands required for arrow
    """
    if c == 'y' or c == 'Y' or c.lower() == 'years' or c.lower() == 'year':
        return 'years'
    if c == 'M' or c.lower() == 'months' or c.lower() == 'month':
        return 'months'
    if c == 'm' or c.lower() == 'minute' or c.lower() == 'minute':
        return 'minutes'
    if c == 'd' or c == 'D' or c.lower() == 'days' or c.lower() == 'day':
        return 'days'
    if c == 'w' or c == 'W' or c.lower() == 'weeks' or c.lower() == 'week':
        return 'weeks'
    if c == 'h' or c == 'H' or c.lower() == 'hours' or c.lower() == 'hour':
        return 'hours'
    if c == 's' or c == 'S' or c.lower() == 'seconds' or c.lower() == 'second':
        return 'seconds'
    if c.lower() == 'n' or c.lower() == 'now':
        raise DateMathException(('Timeunit: "{0}" is not valid.  If you are trying to specify \'now\' after timestamp (i.e. 2016-01-01||now/d) that is not valid.  Please try 2016-01-01||/d instead').format(c))
    else:
        raise DateMathException(('Not a valid timeunit: {0}').format(c))


def as_datetime(expression, now, tz='UTC'):
    """
        returs our datemath expression as a python datetime object
        note: this has been deprecated and the 'type' argument in parse is the current way
    """
    return parse(expression, now, tz)


def parse(expression, now=None, tz='UTC', type=None, roundDown=True):
    """
        the main meat and potatoes of this this whole thing
        takes our datemath expression and does our date math
        :param expression - the datemath expression
        :param now - what time is now; when will now be then?  soon
        :param type - if we are dealing with a arrow or datetime object
        :param roundDown - wether or not we should round up or round down on this.  default is roundDown=True, which means if it was 12:00:00, `/d` would be '00:00:00', and with roundDown=False, `/d` would be '29:59:59'
    """
    if now is None:
        now = arrow.utcnow()
    if debug:
        print ('Orig Expression: {0}').format(expression)
    math = ''
    time = ''
    if 'UTC' not in tz:
        if debug:
            print ('will now convert tz to {0}').format(tz)
        now = now.to(tz)
    if expression == 'now':
        if debug:
            print ('Now, no dm: {0}').format(now)
        if type:
            return getattr(now, type)
        return now
    else:
        if re.match('\\d{10,}', str(expression)):
            if debug:
                print 'found an epoch timestamp'
            if len(str(expression)) == 13:
                raise DateMathException('Unable to parse epoch timestamps in millis, please convert to the nearest second to continue - i.e. 1451610061 / 1000')
            ts = arrow.get(int(expression))
            ts = ts.replace(tzinfo=tz)
            return ts
        if expression.startswith('now'):
            math = expression[3:]
            time = now
            if debug:
                print ('now expression: {0}').format(now)
        elif '||' in expression:
            timestamp, math = expression.split('||')
            time = parseTime(timestamp, tz)
        elif expression.startswith(('+', '-', '/')):
            math = expression
            time = now
        else:
            math = ''
            time = parseTime(expression, tz)
    if not math or math == '':
        rettime = time
    rettime = evaluate(math, time, tz, roundDown)
    if type:
        return getattr(rettime, type)
    else:
        return rettime
        return


def parseTime(timestamp, timezone='UTC'):
    """
        parses a date/time stamp and returns and arrow object
    """
    if timestamp and len(timestamp) >= 4:
        ts = arrow.get(timestamp)
        ts = ts.replace(tzinfo=timezone)
        return ts


def roundDate(now, unit, tz='UTC', roundDown=True):
    """
        rounds our date object
    """
    if roundDown:
        now = now.floor(unit)
    else:
        now = now.ceil(unit)
    if debug:
        print ('roundDate Now: {0}').format(now)
    return now


def calculate(now, offsetval, unit):
    """
        calculates our dateobject using arrows replace method
        see unitMap() for more details
    """
    if unit not in ('days', 'hours', 'seconds'):
        offsetval = int(offsetval)
    try:
        now = now.shift(**{unit: offsetval})
        if debug:
            print ('Calculate called:  now: {}, offsetval: {}, offsetval-type: {}, unit: {}').format(now, offsetval, type(offsetval), unit)
        return now
    except Exception as e:
        raise DateMathException(('Unable to calculate date: now: {0}, offsetvalue: {1}, unit: {2} - reason: {3}').format(now, offsetval, unit, e))


def evaluate(expression, now, timeZone='UTC', roundDown=True):
    """
        evaluates our datemath style expression
    """
    if debug:
        print ('Expression: {0}').format(expression)
    if debug:
        print ('Now: {0}').format(now)
    val = 0
    i = 0
    while i < len(expression):
        char = expression[i]
        if '/' in char:
            next = str(expression[(i + 1)])
            i += 1
            now = roundDate(now, unitMap(next).rstrip('s'), timeZone, roundDown)
        elif char == '+' or char == '-':
            val = 0
            try:
                m = re.match('(\\d*[.]?\\d+)[\\w+-/]', expression[i + 1:])
                if m:
                    num = m.group(1)
                    val = val * 10 + float(num)
                    i = i + len(num)
                else:
                    raise DateMathException("Unable to determine a proper time qualifier.  Do you have a proper numerical number followed by a valid time unit? i.e. '+1d', '-3d/d', etc.")
            except Exception as e:
                raise DateMathException(('Invalid datematch: What I got was - re.match: {0}, expression: {1}, error: {2}').format(expression[i + 1:], expression, e))

            if char == '+':
                val = float(val)
            else:
                val = float(-val)
        elif re.match('[a-zA-Z]+', char):
            now = calculate(now, val, unitMap(char))
        else:
            raise DateMathException(("'{}' is not a valid timeunit for expression: '{}' ").format(char, expression))
        i += 1

    if debug:
        print ('Fin: {0}').format(now)
    if debug:
        print '\n\n'
    return now


if __name__ == '__main__':
    if debug:
        print ('NOW: {0}').format(arrow.utcnow())
    if debug:
        print '\n\n'