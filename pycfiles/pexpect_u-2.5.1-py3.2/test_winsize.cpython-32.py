# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/thomas/Code/pexpect/pexpect/build/lib/pexpect/tests/test_winsize.py
# Compiled at: 2011-11-02 15:34:09
import pexpect, unittest
from . import PexpectTestCase
import time, sys, os, signal

class TestCaseWinsize(PexpectTestCase.PexpectTestCase):

    def test_winsize(self):
        """
        This tests that the child process can set and get the windows size.
        This makes use of an external script sigwinch_report.py.
        """
        p1 = pexpect.spawn('%s sigwinch_report.py' % self.PYTHONBIN)
        time.sleep(10)
        p1.setwinsize(11, 22)
        time.sleep(3)
        index = p1.expect([pexpect.TIMEOUT, 'SIGWINCH: \\(([0-9]*), ([0-9]*)\\)'], timeout=30)
        if index == 0:
            self.fail('TIMEOUT -- this platform may not support sigwinch properly.\n' + str(p1))
        r = p1.match.group(1)
        c = p1.match.group(2)
        assert r == '11' and c == '22'
        time.sleep(1)
        p1.setwinsize(24, 80)
        index = p1.expect([pexpect.TIMEOUT, 'SIGWINCH: \\(([0-9]*), ([0-9]*)\\)'], timeout=10)
        if index == 0:
            self.fail('TIMEOUT -- this platform may not support sigwinch properly.\n' + str(p1))
        r = p1.match.group(1)
        c = p1.match.group(2)
        assert r == '24' and c == '80'
        p1.close()


if __name__ == '__main__':
    unittest.main()
suite = unittest.makeSuite(TestCaseWinsize, 'test')