# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/thomas/Code/pexpect/pexpect/build/lib/pexpect/tests/test_run.py
# Compiled at: 2011-11-02 15:34:08
import pexpect, unittest, subprocess, sys
from . import PexpectTestCase

def timeout_callback(d):
    if d['event_count'] > 5:
        return 1
    return 0


class ExpectTestCase(PexpectTestCase.PexpectTestCase):

    def test_run_exit(self):
        data, exitstatus = pexpect.run('python exit1.py', withexitstatus=1)
        assert exitstatus == 1, "Exit status of 'python exit1.py' should be 1."

    def test_run(self):
        the_old_way = subprocess.getoutput('ls -l /bin')
        the_new_way, exitstatus = pexpect.run('ls -l /bin', withexitstatus=1)
        the_new_way = the_new_way.replace('\r', '')[:-1]
        assert the_old_way == the_new_way
        assert exitstatus == 0

    def test_run_callback(self):
        pexpect.run('cat', timeout=1, events={pexpect.TIMEOUT: timeout_callback})

    def test_run_bad_exitstatus(self):
        the_new_way, exitstatus = pexpect.run('ls -l /najoeufhdnzkxjd', withexitstatus=1)
        assert exitstatus != 0


if __name__ == '__main__':
    unittest.main()
suite = unittest.makeSuite(ExpectTestCase, 'test')