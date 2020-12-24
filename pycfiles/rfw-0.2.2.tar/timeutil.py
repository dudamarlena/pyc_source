# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sk/seckiss/rfw/rfw/timeutil.py
# Compiled at: 2014-03-26 05:26:53
import re

def parse_interval(t):
    """Parse time interval t given as string in one of the following formats:
    - <number> representing number of seconds
    - <number>s representing number of seconds
    - <number>h representing number of hours
    - <number>d representing number of days
    Time can only be non-negative
    return converted number of seconds as integer or None if wrong format
    """
    t = t.strip()
    m = re.match('(\\d{1,9})([smhd]?)$', t)
    if not m:
        return None
    else:
        t = int(m.group(1))
        unit = m.group(2)
        multiplier = 1
        if unit == 'm':
            multiplier = 60
        elif unit == 'h':
            multiplier = 3600
        elif unit == 'd':
            multiplier = 86400
        return t * multiplier