# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/conrad/prog/galileo-engineio/venv/lib/python3.6/site-packages/tests/common/test_payload.py
# Compiled at: 2019-08-30 19:22:58
# Size of source mod 2**32: 2084 bytes
import unittest, six
from engineio import packet
from engineio import payload

class TestPayload(unittest.TestCase):

    def test_encode_empty_payload(self):
        p = payload.Payload()
        self.assertEqual(p.packets, [])
        self.assertEqual(p.encode(), b'')

    def test_decode_empty_payload(self):
        p = payload.Payload(encoded_payload=b'')
        self.assertEqual(p.encode(), b'')

    def test_encode_payload_xhr2(self):
        pkt = packet.Packet((packet.MESSAGE), data=(six.text_type('abc')))
        p = payload.Payload([pkt])
        self.assertEqual(p.packets, [pkt])
        self.assertEqual(p.encode(), b'\x00\x04\xff4abc')

    def test_decode_payload_xhr2(self):
        p = payload.Payload(encoded_payload=b'\x00\x04\xff4abc')
        self.assertEqual(p.encode(), b'\x00\x04\xff4abc')

    def test_encode_payload_xhr_text(self):
        pkt = packet.Packet((packet.MESSAGE), data=(six.text_type('abc')))
        p = payload.Payload([pkt])
        self.assertEqual(p.packets, [pkt])
        self.assertEqual(p.encode(b64=True), b'4:4abc')

    def test_decode_payload_xhr_text(self):
        p = payload.Payload(encoded_payload=b'4:4abc')
        self.assertEqual(p.encode(), b'\x00\x04\xff4abc')

    def test_encode_payload_xhr_binary(self):
        pkt = packet.Packet((packet.MESSAGE), data=b'\x00\x01\x02', binary=True)
        p = payload.Payload([pkt])
        self.assertEqual(p.packets, [pkt])
        self.assertEqual(p.encode(b64=True), b'6:b4AAEC')

    def test_decode_payload_xhr_binary(self):
        p = payload.Payload(encoded_payload=b'6:b4AAEC')
        self.assertEqual(p.encode(), b'\x01\x04\xff\x04\x00\x01\x02')

    def test_decode_invalid_payload(self):
        self.assertRaises(ValueError, (payload.Payload), encoded_payload=b'bad payload')

    def test_decode_multi_payload(self):
        p = payload.Payload(encoded_payload=b'4:4abc\x00\x04\xff4def')
        self.assertEqual(len(p.packets), 2)
        self.assertEqual(p.packets[0].data, 'abc')
        self.assertEqual(p.packets[1].data, 'def')