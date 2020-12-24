# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/tests/ipv6/messages/test_request_message.py
# Compiled at: 2017-06-23 17:22:45
# Size of source mod 2**32: 6002 bytes
"""
Test the RequestMessage implementation
"""
import codecs, unittest
from ipaddress import IPv6Address, IPv6Network
from dhcpkit.ipv6.duids import LinkLayerDUID, LinkLayerTimeDUID
from dhcpkit.ipv6.extensions.dns import OPTION_DNS_SERVERS
from dhcpkit.ipv6.extensions.ntp import OPTION_NTP_SERVER
from dhcpkit.ipv6.extensions.prefix_delegation import IAPDOption, IAPrefixOption, OPTION_IA_PD
from dhcpkit.ipv6.extensions.sntp import OPTION_SNTP_SERVERS
from dhcpkit.ipv6.extensions.sol_max_rt import OPTION_INF_MAX_RT, OPTION_SOL_MAX_RT
from dhcpkit.ipv6.messages import RequestMessage
from dhcpkit.ipv6.options import ClientIdOption, ElapsedTimeOption, IAAddressOption, IANAOption, OPTION_IA_NA, OPTION_VENDOR_OPTS, OptionRequestOption, ReconfigureAcceptOption, ServerIdOption, VendorClassOption
from dhcpkit.tests.ipv6.messages import test_client_server_message
request_message = RequestMessage(transaction_id=bytes.fromhex('f350d6'), options=[
 ElapsedTimeOption(elapsed_time=104),
 ClientIdOption(duid=LinkLayerDUID(hardware_type=1, link_layer_address=bytes.fromhex('3431c43cb2f1'))),
 ServerIdOption(duid=LinkLayerTimeDUID(hardware_type=1, time=488458703, link_layer_address=bytes.fromhex('00137265ca42'))),
 IANAOption(iaid=bytes.fromhex('c43cb2f1'), options=[
  IAAddressOption(address=IPv6Address('2001:db8:ffff:1:c::e09c'), preferred_lifetime=375, valid_lifetime=600)]),
 IAPDOption(iaid=bytes.fromhex('c43cb2f1'), options=[
  IAPrefixOption(prefix=IPv6Network('2001:db8:ffcc:fe00::/56'), preferred_lifetime=375, valid_lifetime=600)]),
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
 VendorClassOption(enterprise_number=872)])
request_packet = codecs.decode('03f350d60008000200680001000a000300013431c43cb2f10002000e000100011d1d49cf00137265ca4200030028c43cb2f100000000000000000005001820010db8ffff0001000c00000000e09c000001770000025800190029c43cb2f10000000000000000001a001900000177000002583820010db8ffccfe000000000000000000001400000006001000170038001f001900030011005200530010000400000368', 'hex')

class RequestMessageTestCase(test_client_server_message.ClientServerMessageTestCase):

    def setUp(self):
        self.packet_fixture = request_packet
        self.message_fixture = request_message
        self.parse_packet()


if __name__ == '__main__':
    unittest.main()