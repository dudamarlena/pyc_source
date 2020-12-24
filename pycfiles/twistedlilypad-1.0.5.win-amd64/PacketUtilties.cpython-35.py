# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Python35\Lib\site-packages\twistedlilypad\Utilities\PacketUtilties.py
# Compiled at: 2015-01-20 10:13:25
# Size of source mod 2**32: 446 bytes
from twistedlilypad.Packets import codecLookup
from twistedlilypad.Packets.AbstractPacket import AbstractPacket
from twistedlilypad.Utilities.EncoderUtilities import varIntEncoder

def makePacketStream(packet):
    assert isinstance(packet, AbstractPacket)
    encodedPacket = codecLookup[packet.opcode].encode(packet)
    opcode = varIntEncoder(packet.opcode)
    return varIntEncoder(len(encodedPacket) + len(opcode)) + opcode + encodedPacket