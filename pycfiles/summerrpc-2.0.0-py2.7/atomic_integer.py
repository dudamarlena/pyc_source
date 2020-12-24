# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summerrpc/helper/atomic_integer.py
# Compiled at: 2018-07-31 10:42:31
__all__ = [
 'AtomicInteger']
__authors__ = ['Tim Chow']
import threading

class AtomicInteger(object):

    def __init__(self, initial):
        self._initial = initial
        self._integer = initial
        self._lock = threading.RLock()
        self._max_int = 4294967296

    def increment(self, increment=1, rotate=False):
        with self._lock:
            self._integer = self._integer + increment
            if rotate and self._integer > self._max_int:
                self._integer = self._initial
            return self._integer

    def get_value(self):
        with self._lock:
            return self._integer

    def compare_and_set(self, expect, update):
        with self._lock:
            if self._integer != expect:
                return False
            else:
                self._integer = update
                return True