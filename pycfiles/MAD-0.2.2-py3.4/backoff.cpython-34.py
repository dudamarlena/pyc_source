# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mad\simulation\backoff.py
# Compiled at: 2016-04-23 08:53:07
# Size of source mod 2**32: 1441 bytes
from random import randint

class BackoffStrategy:

    def delay(self, attempt):
        raise NotImplementedError('BackoffStrategy::delay is abstract!')


class ConstantBackoff(BackoffStrategy):

    def __init__(self, base_delay):
        self.base_delay = base_delay

    def delay(self, attempts):
        return self.base_delay


class ExponentialBackoff(ConstantBackoff):

    def __init__(self, base_delay):
        super().__init__(base_delay)

    def delay(self, attempts):
        if attempts == 0:
            return 0
        else:
            limit = 2 ** attempts - 1
            return self._pick_up_to(limit) * self.base_delay

    @staticmethod
    def _pick_up_to(limit):
        return randint(0, limit)