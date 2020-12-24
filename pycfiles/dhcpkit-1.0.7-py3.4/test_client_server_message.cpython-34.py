# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/tests/ipv6/messages/test_client_server_message.py
# Compiled at: 2017-06-23 17:22:45
# Size of source mod 2**32: 3991 bytes
"""
Test the ClientServerMessage implementation
"""
import unittest
from dhcpkit.ipv6.duids import EnterpriseDUID
from dhcpkit.ipv6.messages import ClientServerMessage, SolicitMessage
from dhcpkit.ipv6.options import ClientIdOption, ElapsedTimeOption, IANAOption, IATAOption, UnknownOption
from dhcpkit.tests.ipv6.messages import test_message
from dhcpkit.tests.ipv6.messages.test_unknown_message import unknown_packet

class ClientServerMessageTestCase(test_message.MessageTestCase):

    def setUp(self):
        self.packet_fixture = bytes.fromhex('0158595a00010015000200009d10444843504b6974556e697454657374000800020000')
        self.message_fixture = SolicitMessage(transaction_id=b'XYZ', options=[
         ClientIdOption(duid=EnterpriseDUID(enterprise_number=40208, identifier=b'DHCPKitUnitTest')),
         ElapsedTimeOption(elapsed_time=0)])
        self.parse_packet()

    def parse_packet(self):
        super().parse_packet()
        self.assertIsInstance(self.message, ClientServerMessage)

    def test_validate_transaction_id(self):
        self.message.transaction_id = b'AB'
        with self.assertRaisesRegex(ValueError, '3 bytes'):
            self.message.validate()
        self.message.transaction_id = b'ABCD'
        with self.assertRaisesRegex(ValueError, '3 bytes'):
            self.message.validate()
        self.message.transaction_id = 'ABC'
        with self.assertRaisesRegex(ValueError, '3 bytes'):
            self.message.validate()

    def test_validate_IAID_uniqueness(self):
        self.message.options.append(IANAOption(iaid=b'test'))
        self.message.validate()
        self.message.options.append(IATAOption(iaid=b'test'))
        self.message.validate()
        self.message.options.append(IATAOption(iaid=b'test'))
        with self.assertRaisesRegex(ValueError, 'not unique'):
            self.message.validate()

    def test_get_options_of_type(self):
        found_options = self.message.get_options_of_type(ClientIdOption)
        self.assertEqual(len(found_options), 1)
        self.assertIsInstance(found_options[0], ClientIdOption)
        found_options = self.message.get_options_of_type(UnknownOption)
        self.assertEqual(len(found_options), 0)

    def test_get_option_of_type(self):
        found_option = self.message.get_option_of_type(ClientIdOption)
        self.assertIsInstance(found_option, ClientIdOption)
        found_option = self.message.get_option_of_type(UnknownOption)
        self.assertIsNone(found_option)

    def test_load_from_wrong_buffer(self):
        message = self.message_class()
        with self.assertRaisesRegex(ValueError, 'buffer does not contain'):
            message.load_from(unknown_packet)


if __name__ == '__main__':
    unittest.main()