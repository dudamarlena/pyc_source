# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/tests/ipv6/options/test_ia_ta_option.py
# Compiled at: 2017-06-23 17:22:45
# Size of source mod 2**32: 3521 bytes
"""
Test the IATAOption implementation
"""
import unittest
from ipaddress import IPv6Address
from dhcpkit.ipv6.options import IAAddressOption, IATAOption, STATUS_SUCCESS, StatusCodeOption, UnknownOption
from dhcpkit.tests.ipv6.options import test_option

class IATAOptionTestCase(test_option.OptionTestCase):

    def setUp(self):
        self.option_bytes = bytes.fromhex('0004003c414243440005001820010db80000000000000000000000010000000000000000000d0018000045766572797468696e6720697320617765736f6d6521')
        self.option_object = IATAOption(iaid=b'ABCD', options=[
         IAAddressOption(address=IPv6Address('2001:db8::1')),
         StatusCodeOption(status_code=STATUS_SUCCESS, status_message='Everything is awesome!')])
        self.parse_option()

    def test_validate_iaid(self):
        self.option.iaid = b'ABC'
        with self.assertRaisesRegex(ValueError, 'must be four bytes'):
            self.option.validate()
        self.option.iaid = b'ABCDE'
        with self.assertRaisesRegex(ValueError, 'must be four bytes'):
            self.option.validate()
        self.option.iaid = 'ABCD'
        with self.assertRaisesRegex(ValueError, 'must be four bytes'):
            self.option.validate()

    def test_bad_option_length(self):
        with self.assertRaisesRegex(ValueError, 'shorter than the minimum length'):
            IATAOption.parse(bytes.fromhex('0004000041424344'))
        with self.assertRaisesRegex(ValueError, 'length does not match'):
            IATAOption.parse(bytes.fromhex('000400054142434400140000'))

    def test_sort(self):
        self.assertFalse(self.option > self.option)
        self.assertTrue(self.option <= self.option)
        with self.assertRaises(TypeError):
            self.assertFalse(self.option > 0)

    def test_get_options_of_type(self):
        found_options = self.option.get_options_of_type(StatusCodeOption)
        self.assertEqual(len(found_options), 1)
        self.assertIsInstance(found_options[0], StatusCodeOption)
        found_options = self.option.get_options_of_type(UnknownOption)
        self.assertEqual(len(found_options), 0)

    def test_get_option_of_type(self):
        found_option = self.option.get_option_of_type(StatusCodeOption)
        self.assertIsInstance(found_option, StatusCodeOption)
        found_option = self.option.get_option_of_type(UnknownOption)
        self.assertIsNone(found_option)

    def test_get_addresses(self):
        addresses = self.option.get_addresses()
        self.assertListEqual(addresses, [IPv6Address('2001:db8::1')])


if __name__ == '__main__':
    unittest.main()