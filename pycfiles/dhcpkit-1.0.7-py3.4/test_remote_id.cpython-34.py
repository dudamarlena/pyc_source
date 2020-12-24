# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/tests/ipv6/extensions/test_remote_id.py
# Compiled at: 2017-06-23 17:22:45
# Size of source mod 2**32: 988 bytes
"""
Test the RemoteIdOption implementation
"""
import unittest
from dhcpkit.ipv6.extensions.remote_id import RemoteIdOption
from dhcpkit.tests.ipv6.options import test_option

class RemoteIdOptionTestCase(test_option.OptionTestCase):

    def setUp(self):
        self.option_bytes = bytes.fromhex('0025000800009d100123abcd')
        self.option_object = RemoteIdOption(40208, bytes.fromhex('0123abcd'))
        self.parse_option()

    def test_enterprise_number(self):
        self.check_unsigned_integer_property('enterprise_number', size=32)

    def test_remote_id(self):
        self.option.remote_id = 'Not bytes'
        with self.assertRaisesRegex(ValueError, 'sequence of bytes'):
            self.option.validate()

    def test_bad_option_length(self):
        with self.assertRaisesRegex(ValueError, 'longer than the available buffer'):
            RemoteIdOption.parse(bytes.fromhex('0025000a00009d10'))


if __name__ == '__main__':
    unittest.main()