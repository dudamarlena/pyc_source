# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/shinkei/backoff.py
# Compiled at: 2019-12-14 12:45:46
# Size of source mod 2**32: 753 bytes
import random, time

class ExponentialBackoff:

    def __init__(self, base=1, *, integral=False):
        self._base = base
        self._exp = 0
        self._max = 10
        self._reset_time = base * 2048
        self._last_invocation = time.monotonic()
        rand = random.Random()
        rand.seed()
        self._randfunc = rand.randrange if integral else rand.uniform

    def delay(self):
        invocation = time.monotonic()
        interval = invocation - self._last_invocation
        self._last_invocation = invocation
        if interval > self._reset_time:
            self._exp = 0
        self._exp = min(self._exp + 1, self._max)
        return self._randfunc(0, self._base * 2 ** self._exp)