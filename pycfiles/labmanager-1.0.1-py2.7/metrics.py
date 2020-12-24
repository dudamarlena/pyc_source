# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/suds/metrics.py
# Compiled at: 2014-02-26 03:37:27
"""
The I{metrics} module defines classes and other resources
designed for collecting and reporting performance metrics.
"""
import time
from logging import getLogger
from math import modf
log = getLogger(__name__)

class Timer:

    def __init__(self):
        self.started = 0
        self.stopped = 0

    def start(self):
        self.started = time.time()
        self.stopped = 0
        return self

    def stop(self):
        if self.started > 0:
            self.stopped = time.time()
        return self

    def duration(self):
        return self.stopped - self.started

    def __str__(self):
        if self.started == 0:
            return 'not-running'
        if self.started > 0 and self.stopped == 0:
            return 'started: %d (running)' % self.started
        duration = self.duration()
        jmod = lambda m: (m[1], m[0] * 1000)
        if duration < 1:
            ms = duration * 1000
            return '%d (ms)' % ms
        if duration < 60:
            m = modf(duration)
            return '%d.%.3d (seconds)' % jmod(m)
        m = modf(duration / 60)
        return '%d.%.3d (minutes)' % jmod(m)