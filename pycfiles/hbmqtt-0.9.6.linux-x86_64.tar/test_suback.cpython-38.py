# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/tests/mqtt/test_suback.py
# Compiled at: 2020-01-25 09:04:28
# Size of source mod 2**32: 1423 bytes
import asyncio, unittest
from hbmqtt.mqtt.suback import SubackPacket, SubackPayload
from hbmqtt.mqtt.packet import PacketIdVariableHeader
from hbmqtt.adapters import BufferReader

class SubackPacketTest(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()

    def test_from_stream(self):
        data = b'\x90\x06\x00\n\x00\x01\x02\x80'
        stream = BufferReader(data)
        message = self.loop.run_until_complete(SubackPacket.from_stream(stream))
        self.assertEqual(message.payload.return_codes[0], SubackPayload.RETURN_CODE_00)
        self.assertEqual(message.payload.return_codes[1], SubackPayload.RETURN_CODE_01)
        self.assertEqual(message.payload.return_codes[2], SubackPayload.RETURN_CODE_02)
        self.assertEqual(message.payload.return_codes[3], SubackPayload.RETURN_CODE_80)

    def test_to_stream(self):
        variable_header = PacketIdVariableHeader(10)
        payload = SubackPayload([
         SubackPayload.RETURN_CODE_00,
         SubackPayload.RETURN_CODE_01,
         SubackPayload.RETURN_CODE_02,
         SubackPayload.RETURN_CODE_80])
        suback = SubackPacket(variable_header=variable_header, payload=payload)
        out = suback.to_bytes()
        self.assertEqual(out, b'\x90\x06\x00\n\x00\x01\x02\x80')