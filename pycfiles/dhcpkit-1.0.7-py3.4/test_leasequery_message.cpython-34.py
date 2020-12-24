# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/tests/ipv6/extensions/leasequery/test_leasequery_message.py
# Compiled at: 2017-06-23 17:22:45
# Size of source mod 2**32: 1858 bytes
"""
Test the LeasequeryMessage implementation
"""
import unittest
from ipaddress import IPv6Address
from dhcpkit.ipv6.duids import LinkLayerDUID
from dhcpkit.ipv6.extensions.leasequery import LQQueryOption, LeasequeryMessage, OPTION_LQ_RELAY_DATA, QUERY_BY_ADDRESS
from dhcpkit.ipv6.options import ClientIdOption, OptionRequestOption
from dhcpkit.tests.ipv6.messages import test_message

class LeasequeryMessageTestCase(test_message.MessageTestCase):

    def setUp(self):
        self.packet_fixture = bytes.fromhex('0ee86f0c0001000a00030001001ee6f77d00002c001701fe80000000000000000000000000000100060002002f')
        self.message_fixture = LeasequeryMessage(transaction_id=bytes.fromhex('e86f0c'), options=[
         ClientIdOption(duid=LinkLayerDUID(hardware_type=1, link_layer_address=bytes.fromhex('001ee6f77d00'))),
         LQQueryOption(query_type=QUERY_BY_ADDRESS, link_address=IPv6Address('fe80::1'), options=[
          OptionRequestOption(requested_options=[OPTION_LQ_RELAY_DATA])])])
        self.parse_packet()


if __name__ == '__main__':
    unittest.main()