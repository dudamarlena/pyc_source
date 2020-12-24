# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/tests/test_basic.py
# Compiled at: 2017-10-31 16:38:29
from .context import fold_to_ascii
import unittest

class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_none(self):
        self.assertEqual(fold_to_ascii.fold(None), '', 'This is expected to return the empty string.')
        return

    def test_bytestring_raises(self):
        with self.assertRaises(TypeError):
            fold_to_ascii.fold('á')

    def test_bytestring_replacement_raises(self):
        with self.assertRaises(TypeError):
            fold_to_ascii.fold('á', 'X')

    def test_fold(self):
        self.assertEqual(fold_to_ascii.fold('á'), 'a')
        self.assertEqual(fold_to_ascii.fold('£'), '')
        self.assertEqual(fold_to_ascii.fold('💩'), '')

    def test_fold_with_replacement(self):
        self.assertEqual(fold_to_ascii.fold('a', 'X'), 'a')
        self.assertEqual(fold_to_ascii.fold('á', 'X'), 'a')
        self.assertEqual(fold_to_ascii.fold('£', 'X'), 'X')
        self.assertEqual(fold_to_ascii.fold('💩'), '')


if __name__ == '__main__':
    unittest.main()