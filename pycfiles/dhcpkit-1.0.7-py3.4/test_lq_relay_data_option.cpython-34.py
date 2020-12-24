# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/tests/ipv6/extensions/leasequery/test_lq_relay_data_option.py
# Compiled at: 2017-06-23 17:22:45
# Size of source mod 2**32: 4705 bytes
"""
Test the LQRelayDataOption implementation
"""
import unittest
from ipaddress import IPv6Address
from dhcpkit.ipv6.extensions.leasequery import LQRelayDataOption
from dhcpkit.ipv6.messages import RelayForwardMessage, SolicitMessage
from dhcpkit.ipv6.options import InterfaceIdOption
from dhcpkit.tests.ipv6.options import test_option

class ClientDataOptionTestCase(test_option.OptionTestCase):

    def setUp(self):
        self.option_bytes = bytes.fromhex('002f003b20010db80000000000000000000000020c0020010db8000000000000000000000002fe800000000000000000000000000022001200054661322f33')
        self.option_object = LQRelayDataOption(peer_address=IPv6Address('2001:db8::2'), relay_message=RelayForwardMessage(hop_count=0, link_address=IPv6Address('2001:db8::2'), peer_address=IPv6Address('fe80::22'), options=[
         InterfaceIdOption(interface_id=b'Fa2/3')]))
        self.parse_option()

    def test_validate_peer_address(self):
        self.option.peer_address = IPv6Address('2001:db8::1')
        self.option.validate()
        with self.assertRaisesRegex(ValueError, 'valid IPv6 address'):
            self.option.peer_address = '2001:db8::1'
            self.option.validate()
        with self.assertRaisesRegex(ValueError, 'valid IPv6 address'):
            self.option.peer_address = bytes.fromhex('fe800000000000000000000000000001')
            self.option.validate()
        with self.assertRaisesRegex(ValueError, 'valid IPv6 address'):
            self.option.peer_address = IPv6Address('ff02::1')
            self.option.validate()
        with self.assertRaisesRegex(ValueError, 'valid IPv6 address'):
            self.option.peer_address = IPv6Address('::1')
            self.option.validate()

    def test_test_wrong_message(self):
        with self.assertRaisesRegex(ValueError, 'must be an IPv6 DHCP message'):
            LQRelayDataOption(peer_address=IPv6Address('2001:db8::2'), relay_message=None).validate()
        with self.assertRaisesRegex(ValueError, 'cannot contain'):
            LQRelayDataOption(peer_address=IPv6Address('2001:db8::2'), relay_message=SolicitMessage()).validate()

    def test_parse_wrong_type(self):
        with self.assertRaisesRegex(ValueError, 'does not contain LQRelayDataOption data'):
            option = LQRelayDataOption()
            option.load_from(b'00020010ff12000000000000000000000000abcd')

    def test_bad_option_length(self):
        with self.assertRaisesRegex(ValueError, 'embedded message has a different length'):
            LQRelayDataOption.parse(bytes.fromhex('002f003a20010db80000000000000000000000020c0020010db8000000000000000000000002fe800000000000000000000000000022001200054661322f33'))
        with self.assertRaisesRegex(ValueError, 'longer than the available buffer'):
            LQRelayDataOption.parse(bytes.fromhex('002f003c20010db80000000000000000000000020c0020010db8000000000000000000000002fe800000000000000000000000000022001200054661322f33'))


if __name__ == '__main__':
    unittest.main()