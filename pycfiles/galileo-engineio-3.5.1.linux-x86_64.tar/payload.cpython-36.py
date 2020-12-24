# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/conrad/prog/galileo-engineio/venv/lib/python3.6/site-packages/engineio/payload.py
# Compiled at: 2019-08-30 19:22:57
# Size of source mod 2**32: 2820 bytes
import six
from . import packet

class Payload(object):
    __doc__ = 'Engine.IO payload.'

    def __init__(self, packets=None, encoded_payload=None):
        self.packets = packets or []
        if encoded_payload is not None:
            self.decode(encoded_payload)

    def encode(self, b64=False):
        """Encode the payload for transmission."""
        encoded_payload = b''
        for pkt in self.packets:
            encoded_packet = pkt.encode(b64=b64)
            packet_len = len(encoded_packet)
            if b64:
                encoded_payload += str(packet_len).encode('utf-8') + b':' + encoded_packet
            else:
                binary_len = b''
                while packet_len != 0:
                    binary_len = six.int2byte(packet_len % 10) + binary_len
                    packet_len = int(packet_len / 10)

                if not pkt.binary:
                    encoded_payload += b'\x00'
                else:
                    encoded_payload += b'\x01'
                encoded_payload += binary_len + b'\xff' + encoded_packet

        return encoded_payload

    def decode(self, encoded_payload):
        """Decode a transmitted payload."""
        self.packets = []
        while encoded_payload:
            if six.byte2int(encoded_payload[0:1]) <= 1:
                packet_len = 0
                i = 1
                while six.byte2int(encoded_payload[i:i + 1]) != 255:
                    packet_len = packet_len * 10 + six.byte2int(encoded_payload[i:i + 1])
                    i += 1

                self.packets.append(packet.Packet(encoded_packet=(encoded_payload[i + 1:i + 1 + packet_len])))
            else:
                i = encoded_payload.find(b':')
                if i == -1:
                    raise ValueError('invalid payload')
                packet_len = int(encoded_payload[0:i])
                pkt = encoded_payload.decode('utf-8', errors='ignore')[i + 1:i + 1 + packet_len].encode('utf-8')
                self.packets.append(packet.Packet(encoded_packet=pkt))
                packet_len = len(pkt)
            encoded_payload = encoded_payload[i + 1 + packet_len:]