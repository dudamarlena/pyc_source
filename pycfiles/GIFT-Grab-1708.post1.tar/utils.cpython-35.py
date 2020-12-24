# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dzhoshkun/ws/GiftGrab/src/tests/utils.py
# Compiled at: 2016-12-08 10:18:32
# Size of source mod 2**32: 1818 bytes
import time, datetime, pygiftgrab as pgg
use_numpy = True
try:
    import numpy as np
except ImportError:
    use_numpy = False

class FrameRateTimer(pgg.IObserver):
    __doc__ = "Descendant of GIFT-Grab's `Observer`, which\n    will listen to `Observable`s for some time and\n    when asked, will report whether data has been\n    sent at the specified frame rate.\n    "

    def __init__(self, frame_rate):
        global use_numpy
        super(FrameRateTimer, self).__init__()
        self._frame_rate = frame_rate
        if use_numpy:
            self._timestamps = np.array([], dtype='datetime64[us]')
        else:
            self._timestamps = []

    def update(self, frame):
        if use_numpy:
            self._timestamps = np.append(self._timestamps, np.datetime64(datetime.datetime.now()))
        else:
            self._timestamps.append(datetime.datetime.now())

    def __bool__(self):
        """Check if updates have been in time intervals
        in line with defined frame rate, also resetting
        all saved timestamps, i.e. ready for next round.
        """
        if use_numpy:
            diffs = self._timestamps[1:] - self._timestamps[:-1]
            if len(diffs) == 0:
                return False
            return np.count_nonzero(diffs > np.timedelta64(1000000 / self._frame_rate, 'us')) == 0
        else:
            pairs = zip(self._timestamps[:-1], self._timestamps[1:])
            diffs = map(lambda p: (p[1] - p[0]).microseconds / 1000.0, pairs)
            del self._timestamps[:]
            return max(diffs) <= 1000.0 / self._frame_rate

    def __nonzero__(self):
        if self.__bool__():
            return 1
        else:
            return 0