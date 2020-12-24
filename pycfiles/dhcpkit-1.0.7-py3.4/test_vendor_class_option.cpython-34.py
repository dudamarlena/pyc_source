# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/tests/ipv6/options/test_vendor_class_option.py
# Compiled at: 2017-06-23 17:22:45
# Size of source mod 2**32: 1393 bytes
"""
Test the VendorClassOption implementation
"""
import unittest
from dhcpkit.ipv6.options import VendorClassOption
from dhcpkit.tests.ipv6.options import test_option

class VendorClassOptionTestCase(test_option.OptionTestCase):

    def setUp(self):
        self.option_bytes = bytes.fromhex('0010001a00009d10') + b'\x00\x05Class' + b'\x00\rAnother Class'
        self.option_object = VendorClassOption(40208, [b'Class', b'Another Class'])
        self.parse_option()

    def test_enterprise_number(self):
        self.check_unsigned_integer_property('enterprise_number', size=32)

    def test_vendor_classes(self):
        self.option.vendor_classes = b'Not a list'
        with self.assertRaisesRegex(ValueError, 'must be a list'):
            self.option.validate()
        self.option.vendor_classes = [b'In a list', b'X' * 65536]
        with self.assertRaisesRegex(ValueError, 'must be a list'):
            self.option.validate()

    def test_bad_option_length(self):
        with self.assertRaisesRegex(ValueError, 'length does not match'):
            VendorClassOption.parse(bytes.fromhex('0010000a00009d10') + b'\x00\x05Class')
        with self.assertRaisesRegex(ValueError, 'length does not match'):
            VendorClassOption.parse(bytes.fromhex('0010000d00009d10') + b'\x00\x05Class\x00\x01X')


if __name__ == '__main__':
    unittest.main()