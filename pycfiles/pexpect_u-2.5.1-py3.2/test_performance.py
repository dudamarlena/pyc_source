# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pexpect/tests/test_performance.py
# Compiled at: 2011-11-02 15:34:09
import unittest, time, pexpect
from . import PexpectTestCase

class PerformanceTestCase(PexpectTestCase.PexpectTestCase):
    """Testing the performance of expect, with emphasis on wading through long
    inputs. """

    def plain_range(self, n):
        e = pexpect.spawn('python')
        self.assertEqual(e.expect('>>>'), 0)
        e.sendline('for n in range(1, %d+1): print n' % n)
        self.assertEqual(e.expect('\\.{3}'), 0)
        e.sendline('')
        self.assertEqual(e.expect(['inquisition', '%d' % n]), 1)

    def window_range(self, n):
        e = pexpect.spawn('python')
        self.assertEqual(e.expect('>>>'), 0)
        e.sendline('for n in range(1, %d+1): print n' % n)
        self.assertEqual(e.expect('\\.{3}'), 0)
        e.sendline('')
        self.assertEqual(e.expect(['inquisition', '%d' % n], searchwindowsize=12), 1)

    def exact_range(self, n):
        e = pexpect.spawn('python')
        self.assertEqual(e.expect_exact(['>>>']), 0)
        e.sendline('for n in range(1, %d+1): print n' % n)
        self.assertEqual(e.expect_exact(['...']), 0)
        e.sendline('')
        self.assertEqual(e.expect_exact(['inquisition', '%d' % n], timeout=520), 1)

    def ewin_range(self, n):
        e = pexpect.spawn('python')
        self.assertEqual(e.expect_exact(['>>>']), 0)
        e.sendline('for n in range(1, %d+1): print n' % n)
        self.assertEqual(e.expect_exact(['...']), 0)
        e.sendline('')
        self.assertEqual(e.expect_exact(['inquisition', '%d' % n], searchwindowsize=12), 1)

    def faster_range(self, n):
        e = pexpect.spawn('python')
        self.assertEqual(e.expect('>>>'), 0)
        e.sendline('range(1, %d+1)' % n)
        self.assertEqual(e.expect(['inquisition', '%d' % n]), 1)

    def test_100000(self):
        start_time = time.time()
        self.plain_range(100000)
        print('100000 calls to plain_range:', time.time() - start_time)
        start_time = time.time()
        self.window_range(100000)
        print('100000 calls to window_range:', time.time() - start_time)
        start_time = time.time()
        self.exact_range(100000)
        print('100000 calls to exact_range:', time.time() - start_time)
        start_time = time.time()
        self.ewin_range(100000)
        print('100000 calls to ewin_range:', time.time() - start_time)
        start_time = time.time()
        self.faster_range(100000)
        print('100000 calls to faster_range:', time.time() - start_time)


if __name__ == '__main__':
    unittest.main()
suite = unittest.makeSuite(PerformanceTestCase, 'test')