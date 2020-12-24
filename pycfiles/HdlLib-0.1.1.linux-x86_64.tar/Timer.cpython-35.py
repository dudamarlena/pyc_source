# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/HdlLib/Utilities/Timer.py
# Compiled at: 2017-07-08 08:29:58
# Size of source mod 2**32: 2036 bytes
from timeit import default_timer
from datetime import datetime

class Timer:

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.timer = default_timer

    def __enter__(self):
        self.start = self.timer()
        return self

    def __exit__(self, *args):
        end = self.timer()
        self.elapsed_secs = end - self.start
        self.elapsed = self.elapsed_secs * 1000
        if self.verbose:
            print('elapsed time: %f ms' % self.elapsed)


def TimeStamp(Format='%Y-%m-%d_%Hh%Mm%Ss'):
    return datetime.now().strftime(Format)


import time

class ProcessTimer:

    def __init__(self, verbose=False):
        self.StartTime = 0
        self.EndTime = 0

    def __enter__(self):
        try:
            self.StartTime = time.process_time()
        except:
            self.StartTime = time.clock()

        return self

    def __exit__(self, *args):
        try:
            self.EndTime = time.process_time()
        except:
            self.EndTime = time.clock()

    def ExecTimeString(self):
        Delta = self.EndTime - self.StartTime
        h = int(Delta / 3600)
        m = int((Delta - h * 3600) / 60)
        s = int(Delta - h * 3600 - m * 60)
        millisecs = int((Delta - h * 3600 - m * 60 - s) * 1000)
        microsec = int((Delta - h * 3600 - m * 60 - s - millisecs / 1000) * 1000000)
        return '{0}h {1}min {2}s {3}ms {4}µs'.format(h, m, s, millisecs, microsec)