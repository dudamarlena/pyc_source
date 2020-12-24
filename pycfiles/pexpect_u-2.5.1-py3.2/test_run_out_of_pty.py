# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pexpect/tests/test_run_out_of_pty.py
# Compiled at: 2011-11-02 15:34:09
import pexpect, unittest, subprocess, sys
from . import PexpectTestCase

class ExpectTestCase(PexpectTestCase.PexpectTestCase):

    def OFF_test_run_out_of_pty(self):
        """This assumes that the tested platform has < 10000 pty devices.
        This test currently does not work under Solaris.
        Under Solaris it runs out of file descriptors first and
        ld.so starts to barf:
            ld.so.1: pt_chmod: fatal: /usr/lib/libc.so.1: Too many open files
        """
        plist = []
        for count in range(0, 10000):
            try:
                plist.append(pexpect.spawn('ls -l'))
            except pexpect.ExceptionPexpect as e:
                for c in range(0, count):
                    plist[c].close()

                return
            except Exception as e:
                self.fail('Expected ExceptionPexpect. ' + str(e))

        self.fail('Could not run out of pty devices. This may be OK.')


if __name__ == '__main__':
    unittest.main()
suite = unittest.makeSuite(ExpectTestCase, 'test')