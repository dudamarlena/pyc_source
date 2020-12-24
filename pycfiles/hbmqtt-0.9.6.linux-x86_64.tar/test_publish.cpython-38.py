# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/tests/mqtt/test_publish.py
# Compiled at: 2020-01-25 09:04:28
# Size of source mod 2**32: 5248 bytes
import asyncio, unittest
from hbmqtt.mqtt.publish import PublishPacket, PublishVariableHeader, PublishPayload
from hbmqtt.adapters import BufferReader
from hbmqtt.mqtt.constants import QOS_0, QOS_1, QOS_2

class PublishPacketTest(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()

    def test_from_stream_qos_0(self):
        data = b'1\x11\x00\x05topic0123456789'
        stream = BufferReader(data)
        message = self.loop.run_until_complete(PublishPacket.from_stream(stream))
        self.assertEqual(message.variable_header.topic_name, 'topic')
        self.assertEqual(message.variable_header.packet_id, None)
        self.assertFalse(message.fixed_header.flags >> 1 & 3)
        self.assertTrue(message.fixed_header.flags & 1)
        self.assertTrue(message.payload.data, b'0123456789')

    def test_from_stream_qos_2(self):
        data = b'7\x13\x00\x05topic\x00\n0123456789'
        stream = BufferReader(data)
        message = self.loop.run_until_complete(PublishPacket.from_stream(stream))
        self.assertEqual(message.variable_header.topic_name, 'topic')
        self.assertEqual(message.variable_header.packet_id, 10)
        self.assertTrue(message.fixed_header.flags >> 1 & 3)
        self.assertTrue(message.fixed_header.flags & 1)
        self.assertTrue(message.payload.data, b'0123456789')

    def test_to_stream_no_packet_id(self):
        variable_header = PublishVariableHeader('topic', None)
        payload = PublishPayload(b'0123456789')
        publish = PublishPacket(variable_header=variable_header, payload=payload)
        out = publish.to_bytes()
        self.assertEqual(out, b'0\x11\x00\x05topic0123456789')

    def test_to_stream_packet(self):
        variable_header = PublishVariableHeader('topic', 10)
        payload = PublishPayload(b'0123456789')
        publish = PublishPacket(variable_header=variable_header, payload=payload)
        out = publish.to_bytes()
        self.assertEqual(out, b'0\x13\x00\x05topic\x00\n0123456789')

    def test_build(self):
        packet = PublishPacket.build('/topic', b'data', 1, False, QOS_0, False)
        self.assertEqual(packet.packet_id, 1)
        self.assertFalse(packet.dup_flag)
        self.assertEqual(packet.qos, QOS_0)
        self.assertFalse(packet.retain_flag)
        packet = PublishPacket.build('/topic', b'data', 1, False, QOS_1, False)
        self.assertEqual(packet.packet_id, 1)
        self.assertFalse(packet.dup_flag)
        self.assertEqual(packet.qos, QOS_1)
        self.assertFalse(packet.retain_flag)
        packet = PublishPacket.build('/topic', b'data', 1, False, QOS_2, False)
        self.assertEqual(packet.packet_id, 1)
        self.assertFalse(packet.dup_flag)
        self.assertEqual(packet.qos, QOS_2)
        self.assertFalse(packet.retain_flag)
        packet = PublishPacket.build('/topic', b'data', 1, True, QOS_0, False)
        self.assertEqual(packet.packet_id, 1)
        self.assertTrue(packet.dup_flag)
        self.assertEqual(packet.qos, QOS_0)
        self.assertFalse(packet.retain_flag)
        packet = PublishPacket.build('/topic', b'data', 1, True, QOS_1, False)
        self.assertEqual(packet.packet_id, 1)
        self.assertTrue(packet.dup_flag)
        self.assertEqual(packet.qos, QOS_1)
        self.assertFalse(packet.retain_flag)
        packet = PublishPacket.build('/topic', b'data', 1, True, QOS_2, False)
        self.assertEqual(packet.packet_id, 1)
        self.assertTrue(packet.dup_flag)
        self.assertEqual(packet.qos, QOS_2)
        self.assertFalse(packet.retain_flag)
        packet = PublishPacket.build('/topic', b'data', 1, False, QOS_0, True)
        self.assertEqual(packet.packet_id, 1)
        self.assertFalse(packet.dup_flag)
        self.assertEqual(packet.qos, QOS_0)
        self.assertTrue(packet.retain_flag)
        packet = PublishPacket.build('/topic', b'data', 1, False, QOS_1, True)
        self.assertEqual(packet.packet_id, 1)
        self.assertFalse(packet.dup_flag)
        self.assertEqual(packet.qos, QOS_1)
        self.assertTrue(packet.retain_flag)
        packet = PublishPacket.build('/topic', b'data', 1, False, QOS_2, True)
        self.assertEqual(packet.packet_id, 1)
        self.assertFalse(packet.dup_flag)
        self.assertEqual(packet.qos, QOS_2)
        self.assertTrue(packet.retain_flag)
        packet = PublishPacket.build('/topic', b'data', 1, True, QOS_0, True)
        self.assertEqual(packet.packet_id, 1)
        self.assertTrue(packet.dup_flag)
        self.assertEqual(packet.qos, QOS_0)
        self.assertTrue(packet.retain_flag)
        packet = PublishPacket.build('/topic', b'data', 1, True, QOS_1, True)
        self.assertEqual(packet.packet_id, 1)
        self.assertTrue(packet.dup_flag)
        self.assertEqual(packet.qos, QOS_1)
        self.assertTrue(packet.retain_flag)
        packet = PublishPacket.build('/topic', b'data', 1, True, QOS_2, True)
        self.assertEqual(packet.packet_id, 1)
        self.assertTrue(packet.dup_flag)
        self.assertEqual(packet.qos, QOS_2)
        self.assertTrue(packet.retain_flag)