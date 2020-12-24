# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\bogglesolver\test\cli_tests.py
# Compiled at: 2014-06-28 23:52:17
# Size of source mod 2**32: 573 bytes
__doc__ = 'Test for the command line interface.'
import unittest
from bogglesolver.cli import main

class TestCli(unittest.TestCase):
    """TestCli"""

    def test_main(self):
        """Verify 'bogglesolver' can be called."""
        self.assertIs(None, main([]))

    def test_main_help(self):
        """Verify 'bogglesolver --help' can be requested."""
        self.assertRaises(SystemExit, main, ['--help'])
        self.assertRaises(SystemExit, main, ['-h'])


if __name__ == '__main__':
    unittest.main()