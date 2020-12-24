# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\test_status.py
# Compiled at: 2019-10-12 01:12:13
# Size of source mod 2**32: 2961 bytes
"""Tests the status module in KomiDL"""
import os, sys, unittest
from unittest.mock import patch
sys.path.append(os.path.abspath('..'))
import komidl.status as status

class StatusTest(unittest.TestCase):
    __doc__ = 'Test the status module in KomiDL'

    def test_yn_lower_y(self):
        """Lowercase 'y' entered in prompt()"""
        with patch('builtins.input', return_value='y') as (_input):
            self.assertEqual(status.prompt('Test msg'), True)

    def test_yn_upper_y(self):
        """Uppercase 'Y' entered in prompt()"""
        with patch('builtins.input', return_value='Y') as (_input):
            self.assertEqual(status.prompt('Test msg'), True)

    def test_yn_lower_n(self):
        """Lowercase 'n' entered in prompt()"""
        with patch('builtins.input', return_value='n') as (_input):
            self.assertEqual(status.prompt('Test msg'), False)

    def test_yn_upper_n(self):
        """Uppercase 'N' entered in prompt()"""
        with patch('builtins.input', return_value='N') as (_input):
            self.assertEqual(status.prompt('Test msg'), False)

    def test_yn_random(self):
        """A character not 'y' or 'n' entered in prompt()"""
        with patch('builtins.input', return_value='q') as (_input):
            self.assertEqual(status.prompt('Test msg'), False)

    def test_yn_empty(self):
        """No character entered in prompt()"""
        with patch('builtins.input', return_value='') as (_input):
            self.assertEqual(status.prompt('Test msg'), False)

    def test_yn_yes_arg(self):
        """Skip the prompt if args.yes is True"""
        self.assertEqual(status.prompt('Test msg', True), True)

    def test_get_bars(self):
        """Test # of bars to display"""
        test_cases = ((50, 100, 50, 25), (50, 100, 33, 16), (50, 100, 100, 50), (50, 100, 0, 0))
        for barsize, gallery_size, current, expected_bars in test_cases:
            actual_bars = status._bar_size(barsize, current, gallery_size)
            self.assertEqual(expected_bars, actual_bars)

    def test_get_percent(self):
        """Test percentage calculations"""
        test_cases = ((100, 50, 50), (100, 23, 23), (100, 100, 100), (100, 0, 0))
        for gallery_size, current, expected_percent in test_cases:
            actual_percent = status._percent(current, gallery_size)
            self.assertEqual(expected_percent, actual_percent)