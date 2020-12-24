# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/tests/ipv6/extensions/leasequery/test_lq_client_link_option.py
# Compiled at: 2017-06-23 17:22:45
# Size of source mod 2**32: 3580 bytes
"""
Test the LQClientLink implementation
"""
import unittest
from ipaddress import IPv6Address
from dhcpkit.ipv6.extensions.leasequery import LQClientLink, LQRelayDataOption
from dhcpkit.tests.ipv6.options import test_option

class ClientDataOptionTestCase(test_option.OptionTestCase):

    def setUp(self):
        self.option_bytes = bytes.fromhex('0030003020010db800000000000000000000000120010db800000000000000000000000220010db8000000000000000000000004')
        self.option_object = LQClientLink(link_addresses=[
         IPv6Address('2001:db8::1'),
         IPv6Address('2001:db8::2'),
         IPv6Address('2001:db8::4')])
        self.parse_option()

    def test_validate_link_addresses(self):
        self.option.link_addresses = [
         IPv6Address('2001:db8::1')]
        self.option.validate()
        with self.assertRaisesRegex(ValueError, 'must be a list'):
            self.option.link_addresses = IPv6Address('2001:db8::1')
            self.option.validate()
        with self.assertRaisesRegex(ValueError, 'valid IPv6 address'):
            self.option.link_addresses = [
             IPv6Address('2001:db8::1'),
             '2001:db8::1']
            self.option.validate()
        with self.assertRaisesRegex(ValueError, 'valid IPv6 address'):
            self.option.link_addresses = [
             bytes.fromhex('fe800000000000000000000000000001'),
             IPv6Address('2001:db8::1')]
            self.option.validate()
        with self.assertRaisesRegex(ValueError, 'valid IPv6 address'):
            self.option.link_addresses = [
             IPv6Address('2001:db8::1'),
             IPv6Address('ff02::1')]
            self.option.validate()
        with self.assertRaisesRegex(ValueError, 'valid IPv6 address'):
            self.option.link_addresses = [
             IPv6Address('::1'),
             IPv6Address('2001:db8::1')]
            self.option.validate()

    def test_parse_wrong_type(self):
        with self.assertRaisesRegex(ValueError, 'does not contain LQClientLink data'):
            option = LQClientLink()
            option.load_from(b'00020010ff12000000000000000000000000abcd')

    def test_bad_option_length(self):
        with self.assertRaisesRegex(ValueError, 'length does not match the combined length'):
            LQRelayDataOption.parse(bytes.fromhex('0030002f20010db800000000000000000000000120010db800000000000000000000000220010db8000000000000000000000004'))
        with self.assertRaisesRegex(ValueError, 'longer than the available buffer'):
            LQRelayDataOption.parse(bytes.fromhex('0030003120010db800000000000000000000000120010db800000000000000000000000220010db8000000000000000000000004'))


if __name__ == '__main__':
    unittest.main()