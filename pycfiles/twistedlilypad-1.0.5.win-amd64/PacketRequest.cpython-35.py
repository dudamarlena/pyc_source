# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Python35\Lib\site-packages\twistedlilypad\Packets\PacketRequest.py
# Compiled at: 2015-09-12 15:47:48
# Size of source mod 2**32: 1156 bytes
from struct import unpack_from, calcsize, pack
from twistedlilypad.Packets.AbstractPacket import AbstractPacket, AbstractPacketCodec

class PacketRequest(AbstractPacket):
    opcode = 1

    def __init__(self, sequenceID, requestID, payload):
        self.sequenceID = sequenceID
        self.requestID = requestID
        self.payload = payload

    @property
    def payloadSize(self):
        return len(self.payload)

    def __eq__(self, other):
        if not isinstance(other, PacketRequest):
            return NotImplemented
        return self.sequenceID == other.sequenceID and self.requestID == other.requestID and self.payload == other.payload


class PacketRequestCodec(AbstractPacketCodec):

    @staticmethod
    def encode(packet):
        assert isinstance(packet, PacketRequest)
        return pack('>iBH', packet.sequenceID, packet.requestID, packet.payloadSize) + packet.payload

    @staticmethod
    def decode(payload):
        sequenceID, requestID, payloadSize = unpack_from('>iBH', payload)
        payload = payload[calcsize('>iBH'):]
        return PacketRequest(sequenceID, requestID, payload)