# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/tests/ipv6/messages/test_solicit_message.py
# Compiled at: 2017-06-23 17:22:45
# Size of source mod 2**32: 4509 bytes
"""
Test the SolicitMessage implementation
"""
import codecs, unittest
from ipaddress import IPv6Network
from dhcpkit.ipv6.duids import LinkLayerDUID
from dhcpkit.ipv6.extensions.dns import OPTION_DNS_SERVERS
from dhcpkit.ipv6.extensions.ntp import OPTION_NTP_SERVER
from dhcpkit.ipv6.extensions.prefix_delegation import IAPDOption, IAPrefixOption, OPTION_IA_PD
from dhcpkit.ipv6.extensions.sntp import OPTION_SNTP_SERVERS
from dhcpkit.ipv6.extensions.sol_max_rt import OPTION_INF_MAX_RT, OPTION_SOL_MAX_RT
from dhcpkit.ipv6.messages import SolicitMessage
from dhcpkit.ipv6.options import ClientIdOption, ElapsedTimeOption, IANAOption, OPTION_IA_NA, OPTION_VENDOR_OPTS, OptionRequestOption, RapidCommitOption, ReconfigureAcceptOption, VendorClassOption
from dhcpkit.tests.ipv6.messages import test_client_server_message
solicit_message = SolicitMessage(transaction_id=bytes.fromhex('f350d6'), options=[
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
 VendorClassOption(enterprise_number=872)])
solicit_packet = codecs.decode('01f350d60008000200000001000a000300013431c43cb2f1000e00000003000cc43cb2f1000000000000000000190029c43cb2f10000000000000000001a001900000000000000000000000000000000000000000000000000001400000006001000170038001f001900030011005200530010000400000368', 'hex')

class SolicitMessageTestCase(test_client_server_message.ClientServerMessageTestCase):

    def setUp(self):
        self.packet_fixture = solicit_packet
        self.message_fixture = solicit_message
        self.parse_packet()


if __name__ == '__main__':
    unittest.main()