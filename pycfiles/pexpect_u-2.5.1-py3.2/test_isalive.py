# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pexpect/tests/test_isalive.py
# Compiled at: 2011-11-02 15:34:08
import pexpect, unittest, sys, os, time
from . import PexpectTestCase

class IsAliveTestCase(PexpectTestCase.PexpectTestCase):

    def test_expect_wait(self):
        """This tests that calling wait on a finished process works as expected.
        """
        p = pexpect.spawn('sleep 3')
        if not p.isalive():
            self.fail('Child process is not alive. It should be.')
        time.sleep(1)
        p.wait()
        if p.isalive():
            self.fail('Child process is not dead. It should be.')
        p = pexpect.spawn('sleep 3')
        if not p.isalive():
            self.fail('Child process is not alive. It should be.')
        p.kill(9)
        time.sleep(1)
        try:
            p.wait()
        except pexpect.ExceptionPexpect as e:
            pass
        else:
            self.fail("Should have raised ExceptionPython because you can't call wait on a dead process.")

    def test_expect_isalive_dead_after_normal_termination(self):
        p = pexpect.spawn('ls')
        p.expect(pexpect.EOF)
        time.sleep(1)
        if p.isalive():
            self.fail('Child process is not dead. It should be.')

    def test_expect_isalive_dead_after_SIGINT(self):
        p = pexpect.spawn('cat', timeout=5)
        if not p.isalive():
            self.fail('Child process is not alive. It should be.')
        p.terminate()
        time.sleep(1)
        p.expect(pexpect.EOF)
        if p.isalive():
            self.fail('Child process is not dead. It should be.')

    def test_expect_isalive_dead_after_SIGKILL(self):
        p = pexpect.spawn('cat', timeout=3)
        if not p.isalive():
            self.fail('Child process is not alive. It should be.')
        p.kill(9)
        time.sleep(1)
        p.expect(pexpect.EOF)
        if p.isalive():
            self.fail('Child process is not dead. It should be.')

    def test_expect_isalive_consistent_multiple_calls(self):
        """This tests that multiple calls to isalive() return same value.
        """
        p = pexpect.spawn('cat')
        if not p.isalive():
            self.fail('Child process is not alive. It should be.')
        if not p.isalive():
            self.fail('Second call. Child process is not alive. It should be.')
        p.kill(9)
        p.expect(pexpect.EOF)
        if p.isalive():
            self.fail('Child process is not dead. It should be.')
        if p.isalive():
            self.fail('Second call. Child process is not dead. It should be.')


if __name__ == '__main__':
    unittest.main()
suite = unittest.makeSuite(IsAliveTestCase, 'test')