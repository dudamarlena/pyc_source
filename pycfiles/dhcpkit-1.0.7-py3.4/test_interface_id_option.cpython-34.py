# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/tests/ipv6/options/test_interface_id_option.py
# Compiled at: 2017-06-23 17:22:45
# Size of source mod 2**32: 838 bytes
"""
Test the InterfaceIdOption implementation
"""
import unittest
from dhcpkit.ipv6.options import InterfaceIdOption
from dhcpkit.tests.ipv6.options import test_option

class UnknownOptionTestCase(test_option.OptionTestCase):

    def setUp(self):
        self.option_bytes = bytes.fromhex('0012001030313233343536373839616263646566')
        self.option_object = InterfaceIdOption(b'0123456789abcdef')
        self.parse_option()

    def test_interface_id(self):
        self.option.interface_id = 'BlaBla'
        with self.assertRaisesRegex(ValueError, 'sequence of bytes'):
            self.option.validate()
        self.option.interface_id = 'X' * 65536
        with self.assertRaisesRegex(ValueError, 'sequence of bytes'):
            self.option.validate()


if __name__ == '__main__':
    unittest.main()