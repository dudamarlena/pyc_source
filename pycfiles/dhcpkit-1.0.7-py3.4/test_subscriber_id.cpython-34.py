# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/tests/ipv6/extensions/test_subscriber_id.py
# Compiled at: 2017-06-23 17:22:45
# Size of source mod 2**32: 1137 bytes
"""
Test the SubscriberIdOption implementation
"""
import unittest
from dhcpkit.ipv6.extensions.subscriber_id import SubscriberIdOption
from dhcpkit.tests.ipv6.options import test_option

class SubscriberIdOptionTestCase(test_option.OptionTestCase):

    def setUp(self):
        self.option_bytes = bytes.fromhex('002600040123abcd')
        self.option_object = SubscriberIdOption(bytes.fromhex('0123abcd'))
        self.parse_option()

    def test_subscriber_id(self):
        self.option.subscriber_id = 'Not bytes'
        with self.assertRaisesRegex(ValueError, 'sequence of bytes'):
            self.option.validate()
        self.option.subscriber_id = b'\x00' * 65535
        self.option.validate()
        self.option.subscriber_id = b'\x00' * 65536
        with self.assertRaisesRegex(ValueError, 'cannot be longer than'):
            self.option.validate()

    def test_bad_option_length(self):
        with self.assertRaisesRegex(ValueError, 'longer than the available buffer'):
            SubscriberIdOption.parse(bytes.fromhex('002600050123abcd'))


if __name__ == '__main__':
    unittest.main()