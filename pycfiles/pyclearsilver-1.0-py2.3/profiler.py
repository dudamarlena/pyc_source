# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pyclearsilver/profiler.py
# Compiled at: 2004-05-24 13:56:39
import time, who_calls, neo_cgi
PROFILER_DATA = []
PROFILER_START = 0
PROFILER_ENABLED = 0
PROFILER_DEPTH = 0

def enable():
    global PROFILER_DATA
    global PROFILER_ENABLED
    global PROFILER_START
    PROFILER_START = time.time()
    PROFILER_ENABLED = 1
    PROFILER_DATA = []


def disable():
    global PROFILER_DATA
    global PROFILER_ENABLED
    global PROFILER_START
    PROFILER_START = 0
    PROFILER_ENABLED = 0
    PROFILER_DATA = []


def hdfExport(prefix, hdf):
    n = 0
    for p in PROFILER_DATA:
        hdf.setValue('%s.%d.when' % (prefix, n), '%5.2f' % p.when)
        hdf.setValue('%s.%d.time' % (prefix, n), '%5.2f' % p.length)
        hdf.setValue('%s.%d.klass' % (prefix, n), p.klass)
        hdf.setValue('%s.%d.what' % (prefix, n), '&nbsp;' * p.depth + p.what)
        hdf.setValue('%s.%d.where' % (prefix, n), neo_cgi.htmlEscape(p.where))


class Profiler:
    __module__ = __name__

    def __init__(self, klass, what):
        global PROFILER_DEPTH
        if not PROFILER_ENABLED:
            return
        self.when = time.time() - PROFILER_START
        self.klass = klass
        self.where = who_calls.pretty_who_calls()
        self.what = what
        self.length = 0
        self.depth = PROFILER_DEPTH
        PROFILER_DEPTH = PROFILER_DEPTH + 1
        PROFILER_DATA.append(self)

    def end(self):
        global PROFILER_DEPTH
        if not PROFILER_ENABLED:
            return
        self.length = time.time() - self.when - PROFILER_START
        PROFILER_DEPTH = PROFILER_DEPTH - 1
        if PROFILER_DEPTH < 0:
            PROFILER_DEPTH = 0


class ProfilerCursor:
    __module__ = __name__

    def __init__(self, real_cursor):
        self.real_cursor = real_cursor

    def execute(self, query, args=None):
        p = Profiler('SQL', query)
        r = self.real_cursor.execute(query, args)
        p.end()
        return r

    def __getattr__(self, key):
        return getattr(self.real_cursor, key)