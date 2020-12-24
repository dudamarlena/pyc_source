# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Python35\Lib\site-packages\twistedlilypad\Packets\PacketRedirectEvent.py
# Compiled at: 2015-09-12 15:30:27
# Size of source mod 2**32: 1093 bytes
from twistedlilypad.Packets.AbstractPacket import AbstractPacket, AbstractPacketCodec
from twistedlilypad.Utilities.DecoderUtilities import varIntPrefixedStringParser
from twistedlilypad.Utilities.EncoderUtilities import varIntPrefixedStringEncoder

class PacketRedirectEvent(AbstractPacket):
    opcode = 4

    def __init__(self, server, player):
        self.server = server
        self.player = player

    def __eq__(self, other):
        if not isinstance(other, PacketRedirectEvent):
            return NotImplemented
        return self.server == other.server and self.player == other.player


class PacketRedirectEventCodec(AbstractPacketCodec):

    @staticmethod
    def encode(packet):
        assert isinstance(packet, PacketRedirectEvent)
        return varIntPrefixedStringEncoder(packet.server) + varIntPrefixedStringEncoder(packet.player)

    @staticmethod
    def decode(payload):
        server, payload = varIntPrefixedStringParser(payload)
        player, payload = varIntPrefixedStringParser(payload)
        return PacketRedirectEvent(server, player)