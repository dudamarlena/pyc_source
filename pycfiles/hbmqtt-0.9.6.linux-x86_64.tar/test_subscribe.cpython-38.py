# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/tests/mqtt/test_subscribe.py
# Compiled at: 2020-01-25 09:04:28
# Size of source mod 2**32: 1324 bytes
import asyncio, unittest
from hbmqtt.mqtt.subscribe import SubscribePacket, SubscribePayload
from hbmqtt.mqtt.packet import PacketIdVariableHeader
from hbmqtt.mqtt.constants import QOS_1, QOS_2
from hbmqtt.adapters import BufferReader

class SubscribePacketTest(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()

    def test_from_stream(self):
        data = b'\x80\x0e\x00\n\x00\x03a/b\x01\x00\x03c/d\x02'
        stream = BufferReader(data)
        message = self.loop.run_until_complete(SubscribePacket.from_stream(stream))
        topic, qos = message.payload.topics[0]
        self.assertEqual(topic, 'a/b')
        self.assertEqual(qos, QOS_1)
        topic, qos = message.payload.topics[1]
        self.assertEqual(topic, 'c/d')
        self.assertEqual(qos, QOS_2)

    def test_to_stream(self):
        variable_header = PacketIdVariableHeader(10)
        payload = SubscribePayload([
         (
          'a/b', QOS_1),
         (
          'c/d', QOS_2)])
        publish = SubscribePacket(variable_header=variable_header, payload=payload)
        out = publish.to_bytes()
        self.assertEqual(out, b'\x82\x0e\x00\n\x00\x03a/b\x01\x00\x03c/d\x02')