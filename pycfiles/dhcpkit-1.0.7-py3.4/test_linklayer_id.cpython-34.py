# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/tests/ipv6/extensions/test_linklayer_id.py
# Compiled at: 2017-06-23 19:34:50
# Size of source mod 2**32: 1599 bytes
"""
Test the RemoteIdOption implementation
"""
import unittest
from dhcpkit.ipv6.extensions.linklayer_id import LinkLayerIdOption
from dhcpkit.tests.ipv6.options import test_option

class LinkLayerIdOptionTestCase(test_option.OptionTestCase):

    def setUp(self):
        self.option_bytes = bytes.fromhex('004f00080001002436ef1d89')
        self.option_object = LinkLayerIdOption(1, bytes.fromhex('002436ef1d89'))
        self.parse_option()

    def test_link_layer_type(self):
        self.check_unsigned_integer_property('link_layer_type', size=16)

    def test_link_layer_address(self):
        self.option.link_layer_address = 'Not bytes'
        with self.assertRaisesRegex(ValueError, 'sequence of bytes'):
            self.option.validate()
        self.option.link_layer_address = b'\x00' * 65533
        self.option.validate()
        self.option.link_layer_address = b'\x00' * 65534
        with self.assertRaisesRegex(ValueError, 'cannot be longer than'):
            self.option.validate()

    def test_display(self):
        output = str(self.option_object)
        self.assertEqual(output, "LinkLayerIdOption(\n  link_layer_type=Ethernet (1),\n  link_layer_address=b'\\x00$6\\xef\\x1d\\x89',\n)")

    def test_bad_option_length(self):
        with self.assertRaisesRegex(ValueError, 'longer than the available buffer'):
            LinkLayerIdOption.parse(bytes.fromhex('004f00090001002436ef1d89'))


if __name__ == '__main__':
    unittest.main()