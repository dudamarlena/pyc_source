# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/tests/utils/test_normalise_hex.py
# Compiled at: 2017-06-24 07:01:50
# Size of source mod 2**32: 1392 bytes
"""
Test the camelcase conversion functions
"""
import unittest
from dhcpkit.utils import normalise_hex

class NormaliseHexTestCase(unittest.TestCase):

    def test_hex(self):
        self.assertEqual(normalise_hex(''), '')
        self.assertEqual(normalise_hex('1a2b3c'), '1a2b3c')
        self.assertEqual(normalise_hex('1a:2b:3c'), '1a2b3c')
        self.assertEqual(normalise_hex('1a:2b3c'), '1a2b3c')
        self.assertEqual(normalise_hex('1a2b:3c'), '1a2b3c')
        self.assertEqual(normalise_hex(bytes.fromhex('1a2b3c')), '1a2b3c')

    def test_hex_with_colons(self):
        self.assertEqual(normalise_hex('', include_colons=True), '')
        self.assertEqual(normalise_hex('1a2b3c', include_colons=True), '1a:2b:3c')
        self.assertEqual(normalise_hex('1a:2b:3c', include_colons=True), '1a:2b:3c')
        self.assertEqual(normalise_hex('1a:2b3c', include_colons=True), '1a:2b:3c')
        self.assertEqual(normalise_hex('1a2b:3c', include_colons=True), '1a:2b:3c')
        self.assertEqual(normalise_hex(bytes.fromhex('1a2b3c'), include_colons=True), '1a:2b:3c')

    def test_bad_hex(self):
        with self.assertRaisesRegex(ValueError, 'not valid hex'):
            normalise_hex('1a2:b3c')
        with self.assertRaisesRegex(ValueError, 'not valid hex'):
            normalise_hex('Something')


if __name__ == '__main__':
    unittest.main()