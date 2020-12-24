# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jenkviz/build.py
# Compiled at: 2012-01-23 16:05:52
from datetime import timedelta
from util import time_to_datetime
from util import duration_to_second
from util import str2id

class Build(object):
    """ Container for activity information"""

    def __init__(self, url, host, name, build_number, start, duration, status, downstream, base_url, trigger):
        self.url = url
        self.host = host
        self.name = name
        self.build_number = build_number
        self.start = start
        self.duration = duration
        self.status = status
        self.downstream = downstream
        self.children = []
        self.base_url = base_url
        self.trigger = trigger
        self.start_t = time_to_datetime(start)
        self.duration_s = duration_to_second(duration)
        self.stop_t = self.start_t + timedelta(seconds=self.duration_s)

    def getId(self):
        return str2id('%s %s' % (self.name, self.build_number))

    def color(self):
        if self.status == 'Success':
            return 'blue'
        if self.status == 'Failure':
            return 'red'
        if self.status == 'Unstable':
            return 'gold'
        return 'black'

    def full_url(self):
        return self.base_url + self.url

    def __repr__(self):
        return 'URL: "%s"\n\tname: %s\n\tbuild #: %s\n\thost: %s\n\tstart: %s\n\tstop: %s\n\tduration: %s\n\tstatus: %s\n\tdownstream build: %d\n' % (
         self.url, self.name, self.build_number, self.host, self.start, self.stop_t, self.duration, self.status,
         len(self.downstream))