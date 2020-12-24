# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/tests/ipv6/messages/test_relay_server_message.py
# Compiled at: 2017-06-24 11:10:26
# Size of source mod 2**32: 7580 bytes
"""
Test the RelayServerMessage implementation
"""
import unittest
from ipaddress import IPv6Address
from dhcpkit.ipv6.messages import Message, RelayForwardMessage, RelayServerMessage, UnknownMessage
from dhcpkit.ipv6.options import RelayMessageOption
from dhcpkit.tests.ipv6.messages import test_message

class RelayServerMessageTestCase(test_message.MessageTestCase):

    def setUp(self):
        self.packet_fixture = bytes.fromhex('0c0220010db800000000000000000002000120010db8000000000000000000020002000900510c0120010db800000000000000000001000120010db80000000000000000000100020009002b0c0020010db800000000000000000000000120010db800000000000000000000000200090005ff41424344')
        self.message_fixture = RelayForwardMessage(hop_count=2, link_address=IPv6Address('2001:db8::2:1'), peer_address=IPv6Address('2001:db8::2:2'), options=[
         RelayMessageOption(relayed_message=RelayForwardMessage(hop_count=1, link_address=IPv6Address('2001:db8::1:1'), peer_address=IPv6Address('2001:db8::1:2'), options=[
          RelayMessageOption(relayed_message=RelayForwardMessage(hop_count=0, link_address=IPv6Address('2001:db8::1'), peer_address=IPv6Address('2001:db8::2'), options=[
           RelayMessageOption(relayed_message=UnknownMessage(255, b'ABCD'))]))]))])
        self.parse_packet()

    def parse_packet(self):
        super().parse_packet()
        self.assertIsInstance(self.message, RelayServerMessage)

    def test_validate_hop_count(self):
        self.check_unsigned_integer_property('hop_count', size=8)

    def test_validate_link_address(self):
        self.message.link_address = bytes.fromhex('20010db8000000000000000000000001')
        with self.assertRaisesRegex(ValueError, 'Link-address .* IPv6 address'):
            self.message.validate()
        self.message.link_address = IPv6Address('ff02::1')
        with self.assertRaisesRegex(ValueError, 'Link-address .* non-multicast IPv6 address'):
            self.message.validate()

    def test_validate_peer_address(self):
        self.message.peer_address = bytes.fromhex('20010db8000000000000000000000001')
        with self.assertRaisesRegex(ValueError, 'Peer-address .* IPv6 address'):
            self.message.validate()
        self.message.peer_address = IPv6Address('ff02::1')
        with self.assertRaisesRegex(ValueError, 'Peer-address .* non-multicast IPv6 address'):
            self.message.validate()

    def test_get_relayed_message(self):
        self.assertEqual(self.message.relayed_message, self.message_fixture.get_option_of_type(RelayMessageOption).relayed_message)

    def test_set_relayed_message(self):
        self.message.options = []
        self.assertEqual(len(self.message.get_options_of_type(RelayMessageOption)), 0)
        self.message.relayed_message = UnknownMessage(255, b'ThisIsAnUnknownMessage')
        self.assertEqual(len(self.message.get_options_of_type(RelayMessageOption)), 1)
        self.assertEqual(self.message.relayed_message.message_data, b'ThisIsAnUnknownMessage')
        self.message.relayed_message = UnknownMessage(255, b'ThisIsADifferentUnknownMessage')
        self.assertEqual(len(self.message.get_options_of_type(RelayMessageOption)), 1)
        self.assertEqual(self.message.relayed_message.message_data, b'ThisIsADifferentUnknownMessage')

    def test_inner_message(self):
        self.assertIsInstance(self.message.inner_message, Message)
        self.assertNotIsInstance(self.message.inner_message, RelayServerMessage)

    def test_inner_relay_message(self):
        self.assertIsInstance(self.message.inner_relay_message, RelayServerMessage)
        self.assertIsInstance(self.message.inner_relay_message.relayed_message, Message)
        self.assertNotIsInstance(self.message.inner_relay_message.relayed_message, RelayServerMessage)

    def test_missing_inner_message(self):
        self.message.inner_relay_message.options = []
        self.assertIsNone(self.message.inner_message)
        self.assertIsInstance(self.message.inner_relay_message, RelayServerMessage)

    def test_empty_inner_message(self):
        self.message.inner_relay_message.get_option_of_type(RelayMessageOption).relayed_message = None
        self.assertIsNone(self.message.inner_message)
        self.assertIsInstance(self.message.inner_relay_message, RelayServerMessage)

    def test_empty_relayed_message(self):
        self.assertIsNotNone(self.message.relayed_message)
        self.message.relayed_message = None
        self.assertIsNone(self.message.relayed_message)
        with self.assertRaisesRegex(ValueError, 'must be an IPv6 DHCP message'):
            self.message.validate()
        option = self.message.get_option_of_type(RelayMessageOption)
        self.message.options.remove(option)
        self.assertIsNone(self.message.relayed_message)


if __name__ == '__main__':
    unittest.main()