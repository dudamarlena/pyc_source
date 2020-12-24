# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Python35\Lib\site-packages\twistedlilypad\Packets\PacketPlayerEvent.py
# Compiled at: 2016-11-30 18:12:09
# Size of source mod 2**32: 1355 bytes
from struct import unpack_from, calcsize
from uuid import UUID
from twistedlilypad.Packets.AbstractPacket import AbstractPacket, AbstractPacketCodec
from twistedlilypad.Utilities.DecoderUtilities import varIntPrefixedStringParser
from twistedlilypad.Utilities.EncoderUtilities import booleanEncoder, varIntPrefixedStringEncoder

class PacketPlayerEvent(AbstractPacket):
    opcode = 6

    def __init__(self, joining, player_name, player_uuid):
        self.joining = joining
        self.player_name = player_name
        self.player_uuid = player_uuid

    def __eq__(self, other):
        if not isinstance(other, PacketPlayerEvent):
            return NotImplemented
        return self.server == other.server and self.player == other.player


class PacketPlayerEventCodec(AbstractPacketCodec):

    @staticmethod
    def encode(packet):
        assert isinstance(packet, PacketPlayerEvent)
        return booleanEncoder(packet.joining) + varIntPrefixedStringEncoder(packet.player_name) + packet.player_uuid.bytes

    @staticmethod
    def decode(payload):
        joining = unpack_from('>B', payload)[0]
        payload = payload[calcsize('>B'):]
        player_name, payload = varIntPrefixedStringParser(payload)
        player_uuid = UUID(bytes=payload[:32])
        return PacketPlayerEvent(joining, player_name, player_uuid)