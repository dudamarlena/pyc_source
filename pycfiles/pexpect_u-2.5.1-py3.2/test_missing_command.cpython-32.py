# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/thomas/Code/pexpect/pexpect/build/lib/pexpect/tests/test_missing_command.py
# Compiled at: 2011-11-02 15:34:08
import pexpect, unittest
from . import PexpectTestCase

class MissingCommandTestCase(PexpectTestCase.PexpectTestCase):

    def testMissingCommand(self):
        try:
            i = pexpect.spawn('ZXQYQZX')
        except Exception:
            pass
        else:
            self.fail('Expected an Exception.')


if __name__ == '__main__':
    unittest.main()
suite = unittest.makeSuite(MissingCommandTestCase, 'test')