# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/botnee/timeout_lock.py
# Compiled at: 2012-04-23 10:25:33
"""
Helper class for a lock with a timeout

Use as follows:

with botnee.timeout_lock.TimeOutLock(botnee_config._timout):
    # do stuff

"""
import threading, time
from botnee import debug

class TimeoutLock(object):

    def __init__(self, lock, timeout):
        self._lock = threading.Lock()
        self._cond = threading.Condition(threading.Lock())
        self._timeout = timeout

    def __enter__(self):
        if self.wait(self._timeout):
            return self
        else:
            return
            return

    def wait(self, timeout, verbose=True):
        self._cond.acquire()
        current_time = start_time = time.time()
        print 'Requesting lock'
        while current_time < start_time + timeout:
            if self._lock.acquire(False):
                debug.print_verbose('Acquired lock', verbose)
                return True
            debug.print_verbose('Waiting for lock', verbose)
            self._cond.wait(timeout - current_time + start_time)
            current_time = time.time()

        return False

    def __exit__(self, type, value, traceback, verbose=True):
        try:
            self._lock.release()
        except Exception:
            pass

        self._cond.notify()
        debug.print_verbose('Released lock', verbose)