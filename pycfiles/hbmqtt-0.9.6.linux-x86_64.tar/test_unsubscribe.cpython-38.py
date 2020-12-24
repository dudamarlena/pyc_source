# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/tests/mqtt/test_unsubscribe.py
# Compiled at: 2020-01-25 09:04:28
# Size of source mod 2**32: 1060 bytes
import asyncio, unittest
from hbmqtt.mqtt.unsubscribe import UnsubscribePacket, UnubscribePayload
from hbmqtt.mqtt.packet import PacketIdVariableHeader
from hbmqtt.adapters import BufferReader

class UnsubscribePacketTest(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()

    def test_from_stream(self):
        data = b'\xa2\x0c\x00\n\x00\x03a/b\x00\x03c/d'
        stream = BufferReader(data)
        message = self.loop.run_until_complete(UnsubscribePacket.from_stream(stream))
        self.assertEqual(message.payload.topics[0], 'a/b')
        self.assertEqual(message.payload.topics[1], 'c/d')

    def test_to_stream(self):
        variable_header = PacketIdVariableHeader(10)
        payload = UnubscribePayload(['a/b', 'c/d'])
        publish = UnsubscribePacket(variable_header=variable_header, payload=payload)
        out = publish.to_bytes()
        self.assertEqual(out, b'\xa2\x0c\x00\n\x00\x03a/b\x00\x03c/d')