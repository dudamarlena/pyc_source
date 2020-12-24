# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rensike/Workspace/icv/icv/utils/time.py
# Compiled at: 2019-07-22 04:34:42
# Size of source mod 2**32: 857 bytes
from time import time, localtime, strftime

class Time(object):

    def __init__(self):
        self.running = False

    @staticmethod
    def now():
        return time()

    @staticmethod
    def now_str():
        return strftime('%Y-%m-%d %H:%M:%S', localtime(time()))

    @staticmethod
    def is_before(t):
        return time() - t < 0

    @staticmethod
    def is_after(t):
        return time() - t > 0

    def start(self):
        self.running = True
        self._t_start = time()
        self._t_last = time()

    def since_start(self):
        if not self.running:
            return 0
        else:
            self._t_last = time()
            return self._t_last - self._t_start

    def since_last(self):
        if not self.running:
            return 0
        else:
            self._t_last = time()
            return self._t_last - self._t_start