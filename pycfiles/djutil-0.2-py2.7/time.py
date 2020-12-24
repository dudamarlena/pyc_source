# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\djutil\time.py
# Compiled at: 2013-08-27 09:34:01
from __future__ import unicode_literals
from django.utils.timezone import now as tznow, localtime

def format_hour(t):
    v = t.strftime(b'%H:%M')
    if v[0] == b'0':
        return v[1:]
    return v


def get_local_time():
    return localtime(tznow())


def get_local_date():
    return get_local_time().date()