# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/thomas/Code/pexpect/pexpect/build/lib/pexpect/tests/test_interact.py
# Compiled at: 2011-11-02 15:34:08
import pexpect, unittest
from . import PexpectTestCase

class InteractTestCase(PexpectTestCase.PexpectTestCase):

    def test_interact(self):
        p = pexpect.spawn('%s interact.py' % self.PYTHONBIN)
        p.sendline('Hello')
        p.sendline('there')
        p.sendline('Mr. Python')
        p.expect('Hello')
        p.expect('there')
        p.expect('Mr. Python')
        p.sendeof()
        p.expect(pexpect.EOF)


if __name__ == '__main__':
    unittest.main()
suite = unittest.makeSuite(InteractTestCase, 'test')