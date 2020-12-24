# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/tests/ipv6/options/test_user_class_option.py
# Compiled at: 2017-06-23 17:22:45
# Size of source mod 2**32: 1230 bytes
"""
Test the UserClassOption implementation
"""
import unittest
from dhcpkit.ipv6.options import UserClassOption
from dhcpkit.tests.ipv6.options import test_option

class UserClassOptionTestCase(test_option.OptionTestCase):

    def setUp(self):
        self.option_bytes = bytes.fromhex('000f0016') + b'\x00\x05Class' + b'\x00\rAnother Class'
        self.option_object = UserClassOption([b'Class', b'Another Class'])
        self.parse_option()

    def test_user_classes(self):
        self.option.user_classes = b'Not a list'
        with self.assertRaisesRegex(ValueError, 'must be a list'):
            self.option.validate()
        self.option.user_classes = [b'In a list', b'X' * 65536]
        with self.assertRaisesRegex(ValueError, 'must be a list'):
            self.option.validate()

    def test_bad_option_length(self):
        with self.assertRaisesRegex(ValueError, 'length does not match'):
            UserClassOption.parse(bytes.fromhex('000f0006') + b'\x00\x05Class')
        with self.assertRaisesRegex(ValueError, 'length does not match'):
            UserClassOption.parse(bytes.fromhex('000f0009') + b'\x00\x05Class\x00\x01X')


if __name__ == '__main__':
    unittest.main()