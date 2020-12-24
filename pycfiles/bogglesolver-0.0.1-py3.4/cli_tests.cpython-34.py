# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\bogglesolver\test\cli_tests.py
# Compiled at: 2014-06-28 23:52:17
# Size of source mod 2**32: 573 bytes
"""Test for the command line interface."""
import unittest
from bogglesolver.cli import main

class TestCli(unittest.TestCase):
    __doc__ = 'Tests for the cli.'

    def test_main(self):
        """Verify 'bogglesolver' can be called."""
        self.assertIs(None, main([]))

    def test_main_help(self):
        """Verify 'bogglesolver --help' can be requested."""
        self.assertRaises(SystemExit, main, ['--help'])
        self.assertRaises(SystemExit, main, ['-h'])


if __name__ == '__main__':
    unittest.main()