# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/tests/mqtt/test_unsuback.py
# Compiled at: 2020-01-25 09:04:28
# Size of source mod 2**32: 863 bytes
import asyncio, unittest
from hbmqtt.mqtt.unsuback import UnsubackPacket
from hbmqtt.mqtt.packet import PacketIdVariableHeader
from hbmqtt.adapters import BufferReader

class UnsubackPacketTest(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()

    def test_from_stream(self):
        data = b'\xb0\x02\x00\n'
        stream = BufferReader(data)
        message = self.loop.run_until_complete(UnsubackPacket.from_stream(stream))
        self.assertEqual(message.variable_header.packet_id, 10)

    def test_to_stream(self):
        variable_header = PacketIdVariableHeader(10)
        publish = UnsubackPacket(variable_header=variable_header)
        out = publish.to_bytes()
        self.assertEqual(out, b'\xb0\x02\x00\n')