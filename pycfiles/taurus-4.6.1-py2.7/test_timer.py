# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/util/test/test_timer.py
# Compiled at: 2019-08-19 15:09:29
"""Test for taurus.core.util.timer"""
__docformat__ = 'restructuredtext'
import time, threading, numpy, unittest
from taurus.core.util.timer import Timer

class TimerTest(unittest.TestCase):
    """Test case for testing the taurus.core.util.timer.Timer class"""

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.__count = 0
        self.__calltimes = []

    def tearDown(self):
        self.__count = 0
        self.__calltimes = []

    def test_calltimes(self):
        """check the quality of the Timer's timing"""
        period = 0.1
        n = 10
        timeout = n * period + 2
        tol = 0.001
        timer = Timer(period, self._callback, None, strict_timing=True, sleep=0.05, n=n)
        self.__nCalls = threading.Event()
        timer.start()
        self.__nCalls.wait(timeout)
        timer.stop()
        self.__nCalls.clear()
        ts = numpy.array(self.__calltimes)
        msg = '%i calls expected (got %i)' % (n, ts.size)
        self.assertEqual(ts.size, n, msg)
        totaltime = ts[(-1)] - ts[0]
        drift = abs(totaltime - (n - 1) * period)
        msg = 'Too much drift (%g). Tolerance=%g' % (drift, tol)
        self.assertLess(drift, tol, msg)
        periods = numpy.diff(ts)
        mean = periods.mean()
        std = periods.std()
        msg = 'Wrong period. Expected: %g +/- %g Got: %g +/- %g' % (period, tol,
         mean, std)
        self.assertAlmostEqual(mean, period, msg=msg, delta=tol)
        self.assertLess(std, tol, msg)
        return

    def _callback(self, sleep=0, n=5):
        """store times at which it has been called, and signal when n calls
        have been done. If sleep>0 is passed, sleep that much in each call """
        self.__calltimes.append(time.time())
        self.__count += 1
        time.sleep(sleep)
        if self.__count == n:
            self.__nCalls.set()


if __name__ == '__main__':
    pass