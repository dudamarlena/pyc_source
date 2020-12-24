# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mattcaldwell/.virtualenvs/autopylot/lib/python2.7/site-packages/autopylot/dateutil.py
# Compiled at: 2013-11-26 22:17:25
from datetime import datetime

def unix_time(dt):
    epoch = datetime.utcfromtimestamp(0)
    delta = dt - epoch
    try:
        total_seconds = delta.total_seconds()
    except:
        total_seconds = delta.days * 86400 + delta.seconds + delta.microseconds / 1000000.0

    return total_seconds


def unix_time_millis(dt):
    return unix_time(dt) * 1000.0