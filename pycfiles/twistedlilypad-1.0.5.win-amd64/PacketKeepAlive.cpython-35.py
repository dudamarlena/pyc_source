# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Python35\Lib\site-packages\twistedlilypad\Packets\PacketKeepAlive.py
# Compiled at: 2015-06-15 16:33:29
# Size of source mod 2**32: 717 bytes
from struct import unpack_from, pack
from twistedlilypad.Packets.AbstractPacket import AbstractPacket, AbstractPacketCodec

class PacketKeepAlive(AbstractPacket):
    opcode = 0

    def __init__(self, random):
        self.random = random

    def __eq__(self, other):
        if not isinstance(other, PacketKeepAlive):
            return NotImplemented
        return self.random == other.random


class PacketKeepAliveCodec(AbstractPacketCodec):

    @staticmethod
    def encode(packet):
        assert isinstance(packet, PacketKeepAlive)
        return pack('>i', packet.random)

    @staticmethod
    def decode(payload):
        random = unpack_from('>i', payload)[0]
        return PacketKeepAlive(random)