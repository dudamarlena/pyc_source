# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/tests/stress/testUtil.py
# Compiled at: 2010-03-22 23:48:32
"""
Stressful unittests for functions and classes in netlogger.util
"""
__author__ = 'Dan Gunter dkgunter@lbl.gov'
__rcsid__ = '$Id: testUtil.py 24358 2010-03-23 03:48:32Z dang $'
import sys, time, unittest
from netlogger.tests import shared
from netlogger.tests.stress.shared import Report
from netlogger import util

class TestCase(shared.BaseTestCase):
    """Unit test cases.
    """
    NOW = time.time()

    def testFIFODict(self):
        """Performance test of FIFODict class
        """
        report = Report(title='FIFO dictionary', col_names=('size', 'pctdup', 'total time',
                                                            'rate', 'ms/add'), col_formats=('%d',
                                                                                            '%d%%',
                                                                                            '%f',
                                                                                            '%d',
                                                                                            '%f'))
        for n in (1000, 10000):
            for pct_same in (0, 1, 10, 100):
                fd = util.FIFODict(n)
                for i in xrange(n):
                    key = self._event(i)
                    newkey = fd.add(key)
                    if not newkey:
                        self.fail("New key '%s' seen as duplicate" % key)

                n_same = n * (pct_same / 100)
                t0 = time.time()
                for i in xrange(n):
                    if i < n_same:
                        key = self._event(i)
                        newkey = fd.add(key)
                        if newkey:
                            self.fail("Duplicate key '%s' seen as new" % key)
                    else:
                        key = self._event(i + n)
                        newkey = fd.add(key)
                        if not newkey:
                            self.fail("New key '%s' seen as duplicate" % key)

                t1 = time.time()
                dt = t1 - t0
                report.values((n, pct_same, dt, n / dt, 1000 * dt / n))

    EVENT_NAMES = ('North.Tom', 'East.Dick', 'South.Harry', 'West.Madge')
    ATTR_LENS = (3, 5, 1, 2, 4)
    ATTR_NAMES = ('foo', 'bar', 'lemonade', 'peanut_butter', 'orange')
    ATTR_VALUES = ('alpha', 'bravo', 'tango')

    def _event(self, num):
        e = 'ts=%lf event=%s level=INFO' % (
         self.NOW + num, self.EVENT_NAMES[(num % len(self.EVENT_NAMES))])
        for i in range(self.ATTR_LENS[(num % len(self.ATTR_LENS))]):
            e += ' %s=%s' % (
             self.ATTR_NAMES[((num + i) % len(self.ATTR_NAMES))],
             self.ATTR_VALUES[((num + i) % len(self.ATTR_VALUES))])

        return e


def suite():
    return shared.suite(TestCase)


if __name__ == '__main__':
    shared.main()