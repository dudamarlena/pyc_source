# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/tests/ipv6/options/test_unknown_option.py
# Compiled at: 2017-06-23 17:26:10
# Size of source mod 2**32: 1138 bytes
"""
Test the UnknownOption implementation
"""
import unittest
from dhcpkit.ipv6.options import UnknownOption
from dhcpkit.tests.ipv6.options import test_option

class UnknownOptionTestCase(test_option.OptionTestCase):

    def setUp(self):
        self.option_bytes = b'\x00\xff\x00\x100123456789abcdef'
        self.option_object = UnknownOption(255, b'0123456789abcdef')
        self.parse_option()

    def test_validate_type(self):
        self.option.option_type = -1
        with self.assertRaisesRegex(ValueError, 'unsigned 16 bit integer'):
            self.option.validate()

    def test_validate_data(self):
        self.option.option_data = '0123456789abcdef'
        with self.assertRaisesRegex(ValueError, 'must be sequence of bytes'):
            self.option.validate()
        self.option.option_data = b'0123456789abcdef' * 10000
        with self.assertRaisesRegex(ValueError, 'cannot be longer than'):
            self.option.validate()

    def test_validate_option_type(self):
        self.check_unsigned_integer_property('option_type', size=16)


if __name__ == '__main__':
    unittest.main()