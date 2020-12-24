# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/tests/mqtt/test_packet.py
# Compiled at: 2020-01-25 09:04:28
# Size of source mod 2**32: 1866 bytes
import unittest, asyncio
from hbmqtt.mqtt.packet import CONNECT, MQTTFixedHeader
from hbmqtt.errors import MQTTException
from hbmqtt.adapters import BufferReader

class TestMQTTFixedHeaderTest(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()

    def test_from_bytes(self):
        data = b'\x10\x7f'
        stream = BufferReader(data)
        header = self.loop.run_until_complete(MQTTFixedHeader.from_stream(stream))
        self.assertEqual(header.packet_type, CONNECT)
        self.assertFalse(header.flags & 8)
        self.assertEqual((header.flags & 6) >> 1, 0)
        self.assertFalse(header.flags & 1)
        self.assertEqual(header.remaining_length, 127)

    def test_from_bytes_with_length(self):
        data = b'\x10\xff\xff\xff\x7f'
        stream = BufferReader(data)
        header = self.loop.run_until_complete(MQTTFixedHeader.from_stream(stream))
        self.assertEqual(header.packet_type, CONNECT)
        self.assertFalse(header.flags & 8)
        self.assertEqual((header.flags & 6) >> 1, 0)
        self.assertFalse(header.flags & 1)
        self.assertEqual(header.remaining_length, 268435455)

    def test_from_bytes_ko_with_length(self):
        data = b'\x10\xff\xff\xff\xff\x7f'
        stream = BufferReader(data)
        with self.assertRaises(MQTTException):
            self.loop.run_until_complete(MQTTFixedHeader.from_stream(stream))

    def test_to_bytes(self):
        header = MQTTFixedHeader(CONNECT, 0, 0)
        data = header.to_bytes()
        self.assertEqual(data, b'\x10\x00')

    def test_to_bytes_2(self):
        header = MQTTFixedHeader(CONNECT, 0, 268435455)
        data = header.to_bytes()
        self.assertEqual(data, b'\x10\xff\xff\xff\x7f')