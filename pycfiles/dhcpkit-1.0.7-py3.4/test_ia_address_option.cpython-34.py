# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/tests/ipv6/options/test_ia_address_option.py
# Compiled at: 2017-06-23 17:22:45
# Size of source mod 2**32: 2279 bytes
"""
Test the IAAddressOption implementation
"""
import unittest
from ipaddress import IPv6Address
from dhcpkit.ipv6.options import IAAddressOption, STATUS_NOT_ON_LINK, StatusCodeOption
from dhcpkit.tests.ipv6.options import test_option

class IAAddressOptionTestCase(test_option.OptionTestCase):

    def setUp(self):
        self.option_bytes = bytes.fromhex('0005003520010db800010023045678900bc0cafe0001518000093a80000d0019000457686572652064696420796f752067657420746861743f')
        self.option_object = IAAddressOption(address=IPv6Address('2001:db8:1:23:456:7890:bc0:cafe'), preferred_lifetime=86400, valid_lifetime=604800, options=[
         StatusCodeOption(STATUS_NOT_ON_LINK, 'Where did you get that?')])
        self.parse_option()

    def test_validate_address(self):
        self.option.address = '2001:db8::1'
        with self.assertRaisesRegex(ValueError, 'routable IPv6 address'):
            self.option.validate()
        self.option.address = IPv6Address('::1')
        with self.assertRaisesRegex(ValueError, 'routable IPv6 address'):
            self.option.validate()
        self.option.address = IPv6Address('fe80::1')
        with self.assertRaisesRegex(ValueError, 'routable IPv6 address'):
            self.option.validate()
        self.option.address = IPv6Address('ff02::1')
        with self.assertRaisesRegex(ValueError, 'routable IPv6 address'):
            self.option.validate()

    def test_validate_preferred_lifetime(self):
        self.check_unsigned_integer_property('preferred_lifetime', size=32)

    def test_validate_valid_lifetime(self):
        self.check_unsigned_integer_property('valid_lifetime', size=32)

    def test_bad_option_length(self):
        with self.assertRaisesRegex(ValueError, 'shorter than the minimum length'):
            IAAddressOption.parse(bytes.fromhex('0005001720010db800010023045678900bc0cafe0001518000093a80'))
        with self.assertRaisesRegex(ValueError, 'length does not match'):
            IAAddressOption.parse(bytes.fromhex('0005001920010db800010023045678900bc0cafe0001518000093a8000140000'))


if __name__ == '__main__':
    unittest.main()