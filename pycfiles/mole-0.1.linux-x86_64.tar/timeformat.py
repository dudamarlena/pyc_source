# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/mole/lib/python2.7/site-packages/mole/helper/timeformat.py
# Compiled at: 2012-06-28 06:14:39
import time, datetime
from dateutil.parser import parse as dateparse

class Timezone(datetime.tzinfo):

    def __init__(self, name='+0000'):
        self.name = name
        seconds = int(name[:-2]) * 3600 + int(name[-2:]) * 60
        self.offset = datetime.timedelta(seconds=seconds)

    def utcoffset(self, dt):
        return self.offset

    def dst(self, dt):
        return datetime.timedelta(0)

    def tzname(self, dt):
        return self.name


class TimeFormat(object):

    def __init__(self, timerepr):
        if timerepr.isdigit():
            self.value = datetime.datetime.fromtimestamp(int(timerepr))
        else:
            try:
                self.value = dateparse(timerepr)
            except ValueError:
                tt = time.strptime(timerepr[:-6], '%d/%b/%Y:%H:%M:%S')
                tt = list(tt[:6]) + [0, Timezone(timerepr[-5:])]
                self.value = datetime.datetime(*tt)

    def __repr__(self):
        return self.value.isoformat()

    def __sub__(self, b):
        return self.value - b.value.replace(tzinfo=self.value.tzinfo)

    def __lt__(self, b):
        return self.value < b.value.replace(tzinfo=self.value.tzinfo)

    def __le__(self, b):
        return self.value <= b.value.replace(tzinfo=self.value.tzinfo)

    def __gt__(self, b):
        return self.value > b.value.replace(tzinfo=self.value.tzinfo)

    def __ge__(self, b):
        return self.value > b.value.replace(tzinfo=self.value.tzinfo)

    def __int__(self):
        return int(self.value.strftime('%s'))


class Timespan(object):

    def __init__(self, timerepr):
        if not timerepr:
            self.time = 0
        elif timerepr[(-1)] == 's':
            self.time = int(timerepr[0:-1])
        elif timerepr[(-1)] == 'm':
            self.time = 60 * int(timerepr[0:-1])
        elif timerepr[(-1)] == 'h':
            self.time = 3600 * int(timerepr[0:-1])
        elif timerepr[(-1)] == 'd':
            self.time = 86400 * int(timerepr[0:-1])
        elif timerepr[(-1)] == 'w':
            self.time = 604800 * int(timerepr[0:-1])
        elif timerepr[(-1)] == 'y':
            self.time = 31536000 * int(timerepr[0:-1])
        else:
            self.time = int(timerepr)
        self.time = datetime.timedelta(0, self.time, 0)

    @property
    def seconds(self):
        return self.time

    def __repr__(self):
        return repr(self.time)