# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Python35\Lib\site-packages\twistedlilypad\Packets\PacketMessageEvent.py
# Compiled at: 2015-09-12 15:30:27
# Size of source mod 2**32: 1922 bytes
from codecs import lookup
from struct import unpack_from, pack
from twistedlilypad.Packets.AbstractPacket import AbstractPacket, AbstractPacketCodec
from twistedlilypad.Utilities.DecoderUtilities import varIntPrefixedStringParser
from twistedlilypad.Utilities.EncoderUtilities import varIntPrefixedStringEncoder
utf8_decoder = lookup('UTF_8').decode
utf8_encoder = lookup('UTF_8').encode

class PacketMessageEvent(AbstractPacket):
    opcode = 3
    _message = None

    def __init__(self, sender, channel, payload):
        self.sender = sender
        self.channel = channel
        self.payload = payload

    def __eq__(self, other):
        if not isinstance(other, PacketMessageEvent):
            return NotImplemented
        return self.sender == other.sender and self.channel == other.channel and self.payload == other.payload

    @property
    def payloadSize(self):
        return len(self.payload)

    @property
    def message(self):
        if self._message is None:
            self._message = utf8_decoder(self.payload)[0]
        return self._message

    @message.setter
    def message(self, message):
        self._message = message
        self.payload = utf8_encoder(message)[0]


class PacketMessageEventCodec(AbstractPacketCodec):

    @staticmethod
    def encode(packet):
        assert isinstance(packet, PacketMessageEvent)
        return varIntPrefixedStringEncoder(packet.sender) + varIntPrefixedStringEncoder(packet.channel) + pack('>H', packet.payloadSize) + packet.payload

    @staticmethod
    def decode(payload):
        sender, payload = varIntPrefixedStringParser(payload)
        channel, payload = varIntPrefixedStringParser(payload)
        payloadSize = unpack_from('>H', payload)[0]
        payload = payload[2:2 + payloadSize]
        return PacketMessageEvent(sender, channel, payload)