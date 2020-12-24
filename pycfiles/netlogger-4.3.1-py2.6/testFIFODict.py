# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/tests/unit/testFIFODict.py
# Compiled at: 2009-12-08 17:43:28
"""
Unittests for FIFODict.py
"""
__author__ = 'Dan Gunter dkgunter@lbl.gov'
__rcsid__ = '$Id: testFIFODict.py 23798 2009-07-14 17:18:22Z dang $'
import time, unittest
from netlogger.tests import shared
from netlogger.util import FIFODict

class TestCase(shared.BaseTestCase):
    """Unit test cases.
    """

    def testAdd(self):
        """The add() method
        """
        n = 2
        fifod = FIFODict(n)
        for i in range(n):
            self.failUnless(fifod.add(i))

        for i in range(n):
            self.failIf(fifod.add(i))

        for i in range(n, 2 * n):
            self.failUnless(fifod.add(i))

        for i in range(n):
            self.failUnless(fifod.add(i))

    def testTiming(self):
        """Time FIFO additions
        """
        SZ = 10000
        N = 2 * SZ
        d = FIFODict(SZ)
        t0 = time.time()
        for i in xrange(N):
            d.add(i)

        t1 = time.time()
        self.debug_('inserting %d items in a FIFO of %d took %lf sec (%lf usec/item)' % (
         N, SZ, t1 - t0, (t1 - t0) / float(N) * 1000000.0))
        self.assert_(t1 - t0 < SZ / 1000, 'your computer is too slow!')


def suite():
    return shared.suite(TestCase)


if __name__ == '__main__':
    shared.main()