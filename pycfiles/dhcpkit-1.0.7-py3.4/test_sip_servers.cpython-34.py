# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/tests/ipv6/extensions/test_sip_servers.py
# Compiled at: 2017-06-23 17:22:45
# Size of source mod 2**32: 3500 bytes
"""
Test the SIP options implementations
"""
import unittest
from ipaddress import IPv6Address
from dhcpkit.ipv6.extensions.sip_servers import SIPServersAddressListOption, SIPServersDomainNameListOption
from dhcpkit.tests.ipv6.options import test_option

class SIPServersDomainNameListOptionTestCase(test_option.OptionTestCase):

    def setUp(self):
        self.option_bytes = bytes.fromhex('0015000d') + b'\x08steffann\x02nl\x00'
        self.option_object = SIPServersDomainNameListOption(domain_names=['steffann.nl.'])
        self.parse_option()

    def test_validate_domain_names(self):
        self.option.domain_names = 'steffann.nl'
        with self.assertRaisesRegex(ValueError, 'must be a list'):
            self.option.validate()
        self.option.domain_names = ['steffann.nl', None]
        with self.assertRaisesRegex(ValueError, 'must be a string'):
            self.option.validate()
        self.option.domain_names = ['x' + '.x' * 126]
        self.option.validate()
        self.option.domain_names = [
         'xx' + '.x' * 126]
        with self.assertRaisesRegex(ValueError, 'Domain too long'):
            self.option.validate()
        self.option.domain_names = ['www.123456789012345678901234567890123456789012345678901234567890123.nl']
        self.option.validate()
        self.option.domain_names = [
         'www.1234567890123456789012345678901234567890123456789012345678901234.nl']
        with self.assertRaisesRegex(ValueError, 'Label too long'):
            self.option.validate()

    def test_bad_option_length(self):
        with self.assertRaisesRegex(ValueError, 'must end with a 0-length label'):
            SIPServersDomainNameListOption.parse(bytes.fromhex('0015000c') + b'\x08steffann\x02nl\x00')
        with self.assertRaisesRegex(ValueError, 'exceeds available buffer'):
            SIPServersDomainNameListOption.parse(bytes.fromhex('0015000e') + b'\x08steffann\x02nl\x00\x01')


class SIPServersAddressListOptionTestCase(test_option.OptionTestCase):

    def setUp(self):
        self.option_bytes = bytes.fromhex('0016002020010db800000000000000000000000120010db8000000000000000000000002')
        self.option_object = SIPServersAddressListOption(sip_servers=[IPv6Address('2001:db8::1'),
         IPv6Address('2001:db8::2')])
        self.parse_option()

    def test_validate_sip_servers(self):
        self.option.sip_servers = IPv6Address('2001:db8::1')
        with self.assertRaisesRegex(ValueError, 'must be a list'):
            self.option.validate()
        self.option.sip_servers = ['2001:db8::1', '2001:db8::2']
        with self.assertRaisesRegex(ValueError, 'IPv6 address'):
            self.option.validate()

    def test_bad_option_length(self):
        with self.assertRaisesRegex(ValueError, 'length must be a multiple of 16'):
            SIPServersAddressListOption.parse(bytes.fromhex('0016000f20010db8000000000000000000000001'))
        with self.assertRaisesRegex(ValueError, 'longer than the available buffer'):
            SIPServersAddressListOption.parse(bytes.fromhex('0016001120010db8000000000000000000000001'))
        with self.assertRaisesRegex(ValueError, 'length must be a multiple of 16'):
            SIPServersAddressListOption.parse(bytes.fromhex('0016001120010db800000000000000000000000100'))


if __name__ == '__main__':
    unittest.main()