# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit_kafka/tests/messages/test_kafka_message.py
# Compiled at: 2016-07-16 12:44:07
# Size of source mod 2**32: 2367 bytes
"""
Test the KafkaMessage implementation
"""
import unittest
from dhcpkit_kafka.messages import UnknownKafkaMessage, KafkaMessage

class KafkaMessageTestCase(unittest.TestCase):

    def setUp(self):
        self.packet_fixture = bytes.fromhex('ff') + b'ThisIsAnUnknownMessage'
        self.message_fixture = UnknownKafkaMessage(255, b'ThisIsAnUnknownMessage')
        self.parse_packet()

    def parse_packet(self):
        self.length, self.message = KafkaMessage.parse(self.packet_fixture)
        self.assertIsInstance(self.message, KafkaMessage)
        self.message_class = type(self.message)

    def test_length(self):
        self.assertEqual(self.length, len(self.packet_fixture))

    def test_parse(self):
        self.assertEqual(self.message, self.message_fixture)

    def test_save_parsed(self):
        self.assertEqual(self.packet_fixture, self.message.save())

    def test_save_fixture(self):
        self.assertEqual(self.packet_fixture, self.message_fixture.save())

    def test_validate(self):
        self.message.validate()

    def check_unsigned_integer_property(self, property_name: str, size: int=None):
        """
        Perform basic verification of validation of an unsigned integer

        :param property_name: The property under test
        :param size: The number of bits of this integer field
        """
        setattr(self.message, property_name, 0.1)
        with self.assertRaisesRegex(ValueError, 'integer'):
            self.message.validate()
        setattr(self.message, property_name, 0)
        self.message.validate()
        setattr(self.message, property_name, -1)
        with self.assertRaisesRegex(ValueError, 'unsigned .* integer'):
            self.message.validate()
        if not size:
            return
        setattr(self.message, property_name, 2 ** size - 1)
        self.message.validate()
        setattr(self.message, property_name, 2 ** size)
        with self.assertRaisesRegex(ValueError, 'unsigned {} bit integer'.format(size)):
            self.message.validate()


if __name__ == '__main__':
    unittest.main()