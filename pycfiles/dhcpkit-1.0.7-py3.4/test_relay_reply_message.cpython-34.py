# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/tests/ipv6/messages/test_relay_reply_message.py
# Compiled at: 2017-06-23 17:22:45
# Size of source mod 2**32: 8234 bytes
"""
Test the RelayReplyMessage implementation
"""
import codecs, unittest
from ipaddress import IPv6Address, IPv6Network
from dhcpkit.ipv6.duids import LinkLayerDUID, LinkLayerTimeDUID
from dhcpkit.ipv6.extensions.dns import RecursiveNameServersOption
from dhcpkit.ipv6.extensions.prefix_delegation import IAPDOption, IAPrefixOption
from dhcpkit.ipv6.messages import AdvertiseMessage, RelayReplyMessage
from dhcpkit.ipv6.options import ClientIdOption, IAAddressOption, IANAOption, InterfaceIdOption, ReconfigureAcceptOption, RelayMessageOption, ServerIdOption
from dhcpkit.tests.ipv6.messages import test_relay_server_message
relayed_advertise_message = RelayReplyMessage(hop_count=1, link_address=IPv6Address('2001:db8:ffff:1::1'), peer_address=IPv6Address('fe80::3631:c4ff:fe3c:b2f1'), options=[
 InterfaceIdOption(interface_id=b'Gi0/0/0'),
 RelayMessageOption(relayed_message=RelayReplyMessage(hop_count=0, link_address=IPv6Address('::'), peer_address=IPv6Address('fe80::3631:c4ff:fe3c:b2f1'), options=[
  InterfaceIdOption(interface_id=b'Fa2/3'),
  RelayMessageOption(relayed_message=AdvertiseMessage(transaction_id=bytes.fromhex('f350d6'), options=[
   IANAOption(iaid=bytes.fromhex('c43cb2f1'), options=[
    IAAddressOption(address=IPv6Address('2001:db8:ffff:1:c::e09c'), preferred_lifetime=375, valid_lifetime=600)]),
   IAPDOption(iaid=bytes.fromhex('c43cb2f1'), options=[
    IAPrefixOption(prefix=IPv6Network('2001:db8:ffcc:fe00::/56'), preferred_lifetime=375, valid_lifetime=600)]),
   ClientIdOption(duid=LinkLayerDUID(hardware_type=1, link_layer_address=bytes.fromhex('3431c43cb2f1'))),
   ServerIdOption(duid=LinkLayerTimeDUID(hardware_type=1, time=488458703, link_layer_address=bytes.fromhex('00137265ca42'))),
   ReconfigureAcceptOption(),
   RecursiveNameServersOption(dns_servers=[IPv6Address('2001:4860:4860::8888')])]))]))])
relayed_advertise_packet = codecs.decode('0d0120010db8ffff00010000000000000001fe800000000000003631c4fffe3cb2f1001200074769302f302f30000900c40d0000000000000000000000000000000000fe800000000000003631c4fffe3cb2f1001200054661322f330009009502f350d600030028c43cb2f100000000000000000005001820010db8ffff0001000c00000000e09c000001770000025800190029c43cb2f10000000000000000001a001900000177000002583820010db8ffccfe0000000000000000000001000a000300013431c43cb2f10002000e000100011d1d49cf00137265ca42001400000017001020014860486000000000000000008888', 'hex')

class RelayedAdvertiseMessageTestCase(test_relay_server_message.RelayServerMessageTestCase):

    def setUp(self):
        self.packet_fixture = relayed_advertise_packet
        self.message_fixture = relayed_advertise_message
        self.parse_packet()


if __name__ == '__main__':
    unittest.main()