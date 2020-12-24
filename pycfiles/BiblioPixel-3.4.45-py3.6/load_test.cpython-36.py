# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/bibliopixel/project/load_test.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 734 bytes
import unittest
from unittest.mock import patch
from bibliopixel.project import load

class LoadTest(unittest.TestCase):

    @patch('platform.system', autospec=True)
    def test_split_path(self, platform):
        platform.return_value = 'Darwin'
        to_split = 'abc;def:ghi;jkl:mn'
        actual = load._split_path(to_split)
        expected = ['abc', 'def', 'ghi', 'jkl', 'mn']
        self.assertEqual(actual, expected)

    @patch('platform.system', autospec=True)
    def test_split_path(self, platform):
        platform.return_value = 'Windows'
        to_split = 'abc;def:ghi;jkl:mn'
        actual = load._split_path(to_split)
        expected = ['abc', 'def:ghi', 'jkl:mn']
        self.assertEqual(actual, expected)