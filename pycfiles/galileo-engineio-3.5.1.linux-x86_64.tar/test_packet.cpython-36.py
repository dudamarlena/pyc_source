# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/conrad/prog/galileo-engineio/venv/lib/python3.6/site-packages/tests/common/test_packet.py
# Compiled at: 2019-08-30 19:22:58
# Size of source mod 2**32: 4213 bytes
import unittest, six
from engineio import packet

class TestPacket(unittest.TestCase):

    def test_encode_default_packet(self):
        pkt = packet.Packet()
        self.assertEqual(pkt.packet_type, packet.NOOP)
        self.assertIsNone(pkt.data)
        self.assertFalse(pkt.binary)
        self.assertEqual(pkt.encode(), b'6')

    def test_decode_default_packet(self):
        pkt = packet.Packet(encoded_packet=b'6')
        self.assertTrue(pkt.encode(), b'6')

    def test_encode_text_packet(self):
        data = six.text_type('text')
        pkt = packet.Packet((packet.MESSAGE), data=data)
        self.assertEqual(pkt.packet_type, packet.MESSAGE)
        self.assertEqual(pkt.data, data)
        self.assertFalse(pkt.binary)
        self.assertEqual(pkt.encode(), b'4text')

    def test_decode_text_packet(self):
        pkt = packet.Packet(encoded_packet=b'4text')
        self.assertEqual(pkt.encode(), b'4text')

    def test_encode_binary_packet(self):
        pkt = packet.Packet((packet.MESSAGE), data=b'\x01\x02\x03', binary=True)
        self.assertEqual(pkt.packet_type, packet.MESSAGE)
        self.assertEqual(pkt.data, b'\x01\x02\x03')
        self.assertTrue(pkt.binary)
        self.assertEqual(pkt.encode(), b'\x04\x01\x02\x03')

    def test_encode_binary_bytearray_packet(self):
        pkt = packet.Packet((packet.MESSAGE), data=(bytearray(b'\x01\x02\x03')), binary=True)
        self.assertEqual(pkt.packet_type, packet.MESSAGE)
        self.assertEqual(pkt.data, b'\x01\x02\x03')
        self.assertTrue(pkt.binary)
        self.assertEqual(pkt.encode(), b'\x04\x01\x02\x03')

    def test_encode_binary_b64_packet(self):
        pkt = packet.Packet((packet.MESSAGE), data=b'\x01\x02\x03\x04', binary=True)
        self.assertEqual(pkt.packet_type, packet.MESSAGE)
        self.assertEqual(pkt.data, b'\x01\x02\x03\x04')
        self.assertTrue(pkt.binary)
        self.assertEqual(pkt.encode(b64=True), b'b4AQIDBA==')

    def test_encode_binary_packet_py3(self):
        pkt = packet.Packet((packet.MESSAGE), data=b'\x01\x02\x03')
        self.assertEqual(pkt.packet_type, packet.MESSAGE)
        self.assertEqual(pkt.data, b'\x01\x02\x03')
        self.assertTrue(pkt.binary)
        self.assertEqual(pkt.encode(), b'\x04\x01\x02\x03')

    def test_decode_binary_packet(self):
        pkt = packet.Packet(encoded_packet=b'\x04\x01\x02\x03')
        self.assertTrue(pkt.encode(), b'\x04\x01\x02\x03')

    def test_decode_binary_bytearray_packet(self):
        pkt = packet.Packet(encoded_packet=(bytearray(b'\x04\x01\x02\x03')))
        self.assertTrue(pkt.encode(), b'\x04\x01\x02\x03')

    def test_decode_binary_b64_packet(self):
        pkt = packet.Packet(encoded_packet=b'b4AAEC')
        self.assertTrue(pkt.encode(), b'\x04\x01\x02\x03')

    def test_encode_json_packet(self):
        pkt = packet.Packet((packet.MESSAGE), data={'a':123,  'b':'456'})
        self.assertEqual(pkt.packet_type, packet.MESSAGE)
        self.assertEqual(pkt.data, {'a':123,  'b':'456'})
        self.assertFalse(pkt.binary)
        self.assertIn(pkt.encode(), [b'4{"a":123,"b":"456"}',
         b'4{"b":"456","a":123}'])

    def test_decode_json_packet(self):
        pkt = packet.Packet(encoded_packet=b'4{"a":123,"b":"456"}')
        self.assertIn(pkt.encode(), [b'4{"a":123,"b":"456"}',
         b'4{"b":"456","a":123}'])

    def test_encode_number_packet(self):
        pkt = packet.Packet((packet.MESSAGE), data=123)
        self.assertEqual(pkt.packet_type, packet.MESSAGE)
        self.assertEqual(pkt.data, 123)
        self.assertFalse(pkt.binary)
        self.assertEqual(pkt.encode(), b'4123')

    def test_decode_number_packet(self):
        pkt = packet.Packet(encoded_packet=b'4123')
        self.assertEqual(pkt.packet_type, packet.MESSAGE)
        self.assertEqual(pkt.data, '123')
        self.assertFalse(pkt.binary)
        self.assertEqual(pkt.encode(), b'4123')