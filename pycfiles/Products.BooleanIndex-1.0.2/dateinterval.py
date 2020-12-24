# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/plone-production-nbf-1/zeocluster/src/Products.BlobNewsItem/Paste-1.7.5.1-py2.6.egg/paste/util/dateinterval.py
# Compiled at: 2012-02-27 07:41:58
__doc__ = '\nDateInterval.py\n\nConvert interval strings (in the form of 1w2d, etc) to\nseconds, and back again.  Is not exactly about months or\nyears (leap years in particular).\n\nAccepts (y)ear, (b)month, (w)eek, (d)ay, (h)our, (m)inute, (s)econd.\n\nExports only timeEncode and timeDecode functions.  \n'
import re
__all__ = [
 'interval_decode', 'interval_encode']
second = 1
minute = second * 60
hour = minute * 60
day = hour * 24
week = day * 7
month = day * 30
year = day * 365
timeValues = {'y': year, 
   'b': month, 
   'w': week, 
   'd': day, 
   'h': hour, 
   'm': minute, 
   's': second}
timeOrdered = timeValues.items()
timeOrdered.sort(lambda a, b: -cmp(a[1], b[1]))

def interval_encode(seconds, include_sign=False):
    """Encodes a number of seconds (representing a time interval)
    into a form like 1h2d3s.

    >>> interval_encode(10)
    '10s'
    >>> interval_encode(493939)
    '5d17h12m19s'
    """
    s = ''
    orig = seconds
    seconds = abs(seconds)
    for (char, amount) in timeOrdered:
        if seconds >= amount:
            (i, seconds) = divmod(seconds, amount)
            s += '%i%s' % (i, char)

    if orig < 0:
        s = '-' + s
    else:
        if not orig:
            return '0'
        if include_sign:
            s = '+' + s
    return s


_timeRE = re.compile('[0-9]+[a-zA-Z]')

def interval_decode(s):
    """Decodes a number in the format 1h4d3m (1 hour, 3 days, 3 minutes)
    into a number of seconds

    >>> interval_decode('40s')
    40
    >>> interval_decode('10000s')
    10000
    >>> interval_decode('3d1w45s')
    864045
    """
    time = 0
    sign = 1
    s = s.strip()
    if s.startswith('-'):
        s = s[1:]
        sign = -1
    elif s.startswith('+'):
        s = s[1:]
    for match in allMatches(s, _timeRE):
        char = match.group(0)[(-1)].lower()
        if not timeValues.has_key(char):
            continue
        time += int(match.group(0)[:-1]) * timeValues[char]

    return time


def allMatches(source, regex):
    """Return a list of matches for regex in source
    """
    pos = 0
    end = len(source)
    rv = []
    match = regex.search(source, pos)
    while match:
        rv.append(match)
        match = regex.search(source, match.end())

    return rv


if __name__ == '__main__':
    import doctest
    doctest.testmod()