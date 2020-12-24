# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/tests/ipv6/messages/test_relay_forward_message.py
# Compiled at: 2017-06-23 17:22:45
# Size of source mod 2**32: 10458 bytes
"""
Test the RelayForwardMessage implementation
"""
import codecs, unittest
from ipaddress import IPv6Address, IPv6Network
from dhcpkit.ipv6.duids import LinkLayerDUID
from dhcpkit.ipv6.extensions.dns import OPTION_DNS_SERVERS
from dhcpkit.ipv6.extensions.ntp import OPTION_NTP_SERVER
from dhcpkit.ipv6.extensions.prefix_delegation import IAPDOption, IAPrefixOption, OPTION_IA_PD
from dhcpkit.ipv6.extensions.remote_id import RemoteIdOption
from dhcpkit.ipv6.extensions.sntp import OPTION_SNTP_SERVERS
from dhcpkit.ipv6.extensions.sol_max_rt import OPTION_INF_MAX_RT, OPTION_SOL_MAX_RT
from dhcpkit.ipv6.messages import RelayForwardMessage, RelayReplyMessage, ReplyMessage, SolicitMessage
from dhcpkit.ipv6.options import ClientIdOption, ElapsedTimeOption, IANAOption, InterfaceIdOption, OPTION_IA_NA, OPTION_VENDOR_OPTS, OptionRequestOption, RapidCommitOption, ReconfigureAcceptOption, RelayMessageOption, VendorClassOption
from dhcpkit.tests.ipv6.messages import test_relay_server_message
from dhcpkit.tests.ipv6.messages.test_reply_message import reply_message
relayed_solicit_message = RelayForwardMessage(hop_count=1, link_address=IPv6Address('2001:db8:ffff:1::1'), peer_address=IPv6Address('fe80::3631:c4ff:fe3c:b2f1'), options=[
 RelayMessageOption(relayed_message=RelayForwardMessage(hop_count=0, link_address=IPv6Address('::'), peer_address=IPv6Address('fe80::3631:c4ff:fe3c:b2f1'), options=[
  RelayMessageOption(relayed_message=SolicitMessage(transaction_id=bytes.fromhex('f350d6'), options=[
   ElapsedTimeOption(elapsed_time=0),
   ClientIdOption(duid=LinkLayerDUID(hardware_type=1, link_layer_address=bytes.fromhex('3431c43cb2f1'))),
   RapidCommitOption(),
   IANAOption(iaid=bytes.fromhex('c43cb2f1')),
   IAPDOption(iaid=bytes.fromhex('c43cb2f1'), options=[
    IAPrefixOption(prefix=IPv6Network('::/0'))]),
   ReconfigureAcceptOption(),
   OptionRequestOption(requested_options=[
    OPTION_DNS_SERVERS,
    OPTION_NTP_SERVER,
    OPTION_SNTP_SERVERS,
    OPTION_IA_PD,
    OPTION_IA_NA,
    OPTION_VENDOR_OPTS,
    OPTION_SOL_MAX_RT,
    OPTION_INF_MAX_RT]),
   VendorClassOption(enterprise_number=872)])),
  InterfaceIdOption(interface_id=b'Fa2/3'),
  RemoteIdOption(enterprise_number=9, remote_id=bytes.fromhex('020023000001000a0003000100211c7d486e'))])),
 InterfaceIdOption(interface_id=b'Gi0/0/0'),
 RemoteIdOption(enterprise_number=9, remote_id=bytes.fromhex('020000000000000a0003000124e9b36e8100'))])
relayed_solicit_packet = codecs.decode('0c0120010db8ffff00010000000000000001fe800000000000003631c4fffe3cb2f1000900c20c0000000000000000000000000000000000fe800000000000003631c4fffe3cb2f10009007901f350d60008000200000001000a000300013431c43cb2f1000e00000003000cc43cb2f1000000000000000000190029c43cb2f10000000000000000001a001900000000000000000000000000000000000000000000000000001400000006001000170038001f001900030011005200530010000400000368001200054661322f330025001600000009020023000001000a0003000100211c7d486e001200074769302f302f300025001600000009020000000000000a0003000124e9b36e8100', 'hex')

class RelayedSolicitMessageTestCase(test_relay_server_message.RelayServerMessageTestCase):

    def setUp(self):
        self.packet_fixture = relayed_solicit_packet
        self.message_fixture = relayed_solicit_message
        self.parse_packet()

    def test_wrap_response(self):
        response = self.message.wrap_response(reply_message)
        self.assertIsInstance(response, RelayReplyMessage)
        self.assertEqual(response.hop_count, 1)
        self.assertEqual(response.link_address, IPv6Address('2001:db8:ffff:1::1'))
        self.assertEqual(response.peer_address, IPv6Address('fe80::3631:c4ff:fe3c:b2f1'))
        one_level_in = response.relayed_message
        self.assertIsInstance(one_level_in, RelayReplyMessage)
        self.assertEqual(one_level_in.hop_count, 0)
        self.assertEqual(one_level_in.link_address, IPv6Address('::'))
        self.assertEqual(one_level_in.peer_address, IPv6Address('fe80::3631:c4ff:fe3c:b2f1'))
        two_levels_in = one_level_in.relayed_message
        self.assertIsInstance(two_levels_in, ReplyMessage)
        self.assertEqual(two_levels_in.transaction_id, b'\xf3P\xd6')


if __name__ == '__main__':
    unittest.main()