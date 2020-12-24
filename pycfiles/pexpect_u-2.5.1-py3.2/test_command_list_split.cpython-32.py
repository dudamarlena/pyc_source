# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/thomas/Code/pexpect/pexpect/build/lib/pexpect/tests/test_command_list_split.py
# Compiled at: 2011-11-02 15:34:08
import pexpect, unittest
from . import PexpectTestCase

class SplitCommandLineTestCase(PexpectTestCase.PexpectTestCase):

    def testSplitSizes(self):
        assert len(pexpect.split_command_line('')) == 0
        assert len(pexpect.split_command_line('one')) == 1
        assert len(pexpect.split_command_line('one two')) == 2
        assert len(pexpect.split_command_line('one  two')) == 2
        assert len(pexpect.split_command_line('one   two')) == 2
        assert len(pexpect.split_command_line('one\\ one')) == 1
        assert len(pexpect.split_command_line("'one one'")) == 1
        assert len(pexpect.split_command_line('one\\"one')) == 1
        assert len(pexpect.split_command_line("This\\' is a\\'\\ test")) == 3


if __name__ == '__main__':
    unittest.main()
suite = unittest.makeSuite(SplitCommandLineTestCase, 'test')