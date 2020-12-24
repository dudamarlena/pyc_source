# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/tests/ipv6/extensions/leasequery/test_lq_query_option.py
# Compiled at: 2017-06-23 19:38:42
# Size of source mod 2**32: 4281 bytes
"""
Test the LQQueryOption implementation
"""
import unittest
from ipaddress import IPv6Address
from dhcpkit.ipv6.extensions.leasequery import LQQueryOption, OPTION_LQ_RELAY_DATA, QUERY_BY_ADDRESS
from dhcpkit.ipv6.options import OptionRequestOption, UnknownOption
from dhcpkit.tests.ipv6.options import test_option

class LQQueryOptionTestCase(test_option.OptionTestCase):

    def setUp(self):
        self.option_bytes = bytes.fromhex('002c001701fe80000000000000000000000000000100060002002f')
        self.option_object = LQQueryOption(query_type=QUERY_BY_ADDRESS, link_address=IPv6Address('fe80::1'), options=[
         OptionRequestOption(requested_options=[OPTION_LQ_RELAY_DATA])])
        self.parse_option()

    def test_parse_wrong_type(self):
        with self.assertRaisesRegex(ValueError, 'does not contain LQQueryOption data'):
            option = LQQueryOption()
            option.load_from(b'00020010ff12000000000000000000000000abcd')

    def test_display(self):
        output = str(self.option_object)
        self.assertEqual(output, 'LQQueryOption(\n  query_type=QueryByAddress (1),\n  link_address=fe80::1,\n  options=[\n    OptionRequestOption(requested_options=[LQRelayDataOption (47)]),\n  ],\n)')

    def test_validate_query_type(self):
        self.check_unsigned_integer_property('query_type', 8)

    def test_validate_link_address(self):
        self.option.link_address = IPv6Address('2001:db8::1')
        self.option.validate()
        with self.assertRaisesRegex(ValueError, 'valid IPv6 address'):
            self.option.link_address = '2001:db8::1'
            self.option.validate()
        with self.assertRaisesRegex(ValueError, 'valid IPv6 address'):
            self.option.link_address = bytes.fromhex('fe800000000000000000000000000001')
            self.option.validate()
        with self.assertRaisesRegex(ValueError, 'valid IPv6 address'):
            self.option.link_address = IPv6Address('ff02::1')
            self.option.validate()
        with self.assertRaisesRegex(ValueError, 'valid IPv6 address'):
            self.option.link_address = IPv6Address('::1')
            self.option.validate()

    def test_bad_option_length(self):
        with self.assertRaisesRegex(ValueError, 'shorter than the minimum length'):
            LQQueryOption.parse(bytes.fromhex('002c001001fe800000000000000000000000000001'))
        with self.assertRaisesRegex(ValueError, 'longer than the available buffer'):
            LQQueryOption.parse(bytes.fromhex('002c001201fe800000000000000000000000000001'))
        with self.assertRaisesRegex(ValueError, 'length does not match'):
            LQQueryOption.parse(bytes.fromhex('002c001601fe80000000000000000000000000000100060002002f'))

    def test_get_options_of_type(self):
        found_options = self.option.get_options_of_type(OptionRequestOption)
        self.assertEqual(len(found_options), 1)
        self.assertIsInstance(found_options[0], OptionRequestOption)
        found_options = self.option.get_options_of_type(UnknownOption)
        self.assertEqual(len(found_options), 0)

    def test_get_option_of_type(self):
        found_option = self.option.get_option_of_type(OptionRequestOption)
        self.assertIsInstance(found_option, OptionRequestOption)
        found_option = self.option.get_option_of_type(UnknownOption)
        self.assertIsNone(found_option)


if __name__ == '__main__':
    unittest.main()