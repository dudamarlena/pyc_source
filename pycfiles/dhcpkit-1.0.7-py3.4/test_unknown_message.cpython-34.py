# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/tests/ipv6/messages/test_unknown_message.py
# Compiled at: 2017-06-23 17:22:45
# Size of source mod 2**32: 1107 bytes
"""
Test the UnknownMessage implementation
"""
import unittest
from dhcpkit.ipv6.messages import UnknownMessage
from dhcpkit.tests.ipv6.messages import test_message
unknown_message = UnknownMessage(255, b'ThisIsAnUnknownMessage')
unknown_packet = bytes.fromhex('ff') + b'ThisIsAnUnknownMessage'

class UnknownMessageTestCase(test_message.MessageTestCase):

    def setUp(self):
        self.packet_fixture = unknown_packet
        self.message_fixture = unknown_message
        self.parse_packet()

    def parse_packet(self):
        super().parse_packet()
        self.assertIsInstance(self.message, UnknownMessage)

    def test_validate_message_type(self):
        self.check_unsigned_integer_property('message_type', size=8)

    def test_validate_data(self):
        self.message.message_data = b''
        self.message.validate()
        self.message.message_data = ''
        with self.assertRaisesRegex(ValueError, 'sequence of bytes'):
            self.message.validate()


if __name__ == '__main__':
    unittest.main()