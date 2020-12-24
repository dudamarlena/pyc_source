# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/tests/ipv6/extensions/leasequery/test_client_data_option.py
# Compiled at: 2017-06-23 17:22:45
# Size of source mod 2**32: 5371 bytes
"""
Test the ClientDataOption implementation
"""
import unittest
from ipaddress import IPv6Address, IPv6Network
from dhcpkit.ipv6.duids import EnterpriseDUID
from dhcpkit.ipv6.extensions.leasequery import CLTTimeOption, ClientDataOption, LQRelayDataOption
from dhcpkit.ipv6.extensions.prefix_delegation import IAPrefixOption
from dhcpkit.ipv6.messages import RelayForwardMessage
from dhcpkit.ipv6.options import ClientIdOption, IAAddressOption, InterfaceIdOption, UnknownOption
from dhcpkit.tests.ipv6.options import test_option

class ClientDataOptionTestCase(test_option.OptionTestCase):

    def setUp(self):
        self.option_bytes = bytes.fromhex('002d009900010015000200009d103031323334353637383961626364650005001820010db800000000000000000000cafe0000070800000e10001a00190000070800000e103020010db8000100000000000000000000002e000400000384002f003b20010db80000000000000000000000020c0020010db8000000000000000000000002fe800000000000000000000000000022001200054661322f33')
        self.option_object = ClientDataOption(options=[
         ClientIdOption(EnterpriseDUID(40208, b'0123456789abcde')),
         IAAddressOption(address=IPv6Address('2001:db8::cafe'), preferred_lifetime=1800, valid_lifetime=3600),
         IAPrefixOption(prefix=IPv6Network('2001:db8:1::/48'), preferred_lifetime=1800, valid_lifetime=3600),
         CLTTimeOption(clt_time=900),
         LQRelayDataOption(peer_address=IPv6Address('2001:db8::2'), relay_message=RelayForwardMessage(hop_count=0, link_address=IPv6Address('2001:db8::2'), peer_address=IPv6Address('fe80::22'), options=[
          InterfaceIdOption(interface_id=b'Fa2/3')]))])
        self.parse_option()

    def test_parse_wrong_type(self):
        with self.assertRaisesRegex(ValueError, 'does not contain ClientDataOption data'):
            option = ClientDataOption()
            option.load_from(b'00020010ff12000000000000000000000000abcd')

    def test_bad_option_length(self):
        with self.assertRaisesRegex(ValueError, 'length does not match'):
            ClientDataOption.parse(bytes.fromhex('002d001800010015000200009d10303132333435363738396162636465'))
        with self.assertRaisesRegex(ValueError, 'longer than the available buffer'):
            ClientDataOption.parse(bytes.fromhex('002d001a00010015000200009d10303132333435363738396162636465'))

    def test_get_options_of_type(self):
        found_options = self.option.get_options_of_type(ClientIdOption)
        self.assertEqual(len(found_options), 1)
        self.assertIsInstance(found_options[0], ClientIdOption)
        found_options = self.option.get_options_of_type(UnknownOption)
        self.assertEqual(len(found_options), 0)

    def test_get_option_of_type(self):
        found_option = self.option.get_option_of_type(ClientIdOption)
        self.assertIsInstance(found_option, ClientIdOption)
        found_option = self.option.get_option_of_type(UnknownOption)
        self.assertIsNone(found_option)


if __name__ == '__main__':
    unittest.main()