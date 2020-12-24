# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/lbusoni/git/palpao/test/fake_time_mod.py
# Compiled at: 2018-01-26 14:00:43
# Size of source mod 2**32: 724 bytes
__version__ = '$Id: fake_time_mod.py 25 2018-01-26 19:00:40Z lbusoni $'

class FakeTimeMod(object):

    def __init__(self, timeInvocationDurationSec=0.05):
        self._currentTime = 0.0
        self._timeInvocationDurationSec = timeInvocationDurationSec
        self._lastSleepDurationSec = None

    def time(self):
        self._currentTime += self._timeInvocationDurationSec
        return self._currentTime

    def sleep(self, sleepDurationSec):
        self._lastSleepDurationSec = sleepDurationSec
        self._currentTime += sleepDurationSec

    def hasSleepBeenInvoked(self):
        return self._lastSleepDurationSec is not None

    def getLastSleepDurationSec(self):
        return self._lastSleepDurationSec