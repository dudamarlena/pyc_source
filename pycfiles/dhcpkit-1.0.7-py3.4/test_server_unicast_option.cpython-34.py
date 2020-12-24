# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/tests/ipv6/options/test_server_unicast_option.py
# Compiled at: 2017-06-23 17:22:45
# Size of source mod 2**32: 1684 bytes
"""
Test the ServerUnicastOption implementation
"""
import unittest
from ipaddress import IPv6Address
from dhcpkit.ipv6.options import ServerUnicastOption
from dhcpkit.tests.ipv6.options import test_option

class ServerUnicastOptionTestCase(test_option.OptionTestCase):

    def setUp(self):
        self.option_bytes = bytes.fromhex('000c001020010db8000000000000000000000001')
        self.option_object = ServerUnicastOption(IPv6Address('2001:db8::1'))
        self.parse_option()

    def test_server_address(self):
        self.option.server_address = bytes.fromhex('20010db8000000000000000000000001')
        with self.assertRaisesRegex(ValueError, 'valid IPv6 address'):
            self.option.validate()
        self.option.server_address = IPv6Address('2001:db8::1')
        self.option.validate()
        self.option.server_address = IPv6Address('::')
        with self.assertRaisesRegex(ValueError, 'valid IPv6 address'):
            self.option.validate()
        self.option.server_address = IPv6Address('::1')
        with self.assertRaisesRegex(ValueError, 'valid IPv6 address'):
            self.option.validate()
        self.option.server_address = IPv6Address('ff02::1')
        with self.assertRaisesRegex(ValueError, 'valid IPv6 address'):
            self.option.validate()

    def test_bad_option_length(self):
        with self.assertRaisesRegex(ValueError, 'must have length 16'):
            ServerUnicastOption.parse(bytes.fromhex('000c000f'))
        with self.assertRaisesRegex(ValueError, 'must have length 16'):
            ServerUnicastOption.parse(bytes.fromhex('000c0011'))


if __name__ == '__main__':
    unittest.main()