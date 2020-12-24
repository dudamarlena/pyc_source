# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pgp/packets/parsers.py
# Compiled at: 2015-08-31 08:17:33
from pgp.armor import ASCIIArmor
from pgp.packets.packets import packet_from_packet_data
from pgp.packets.packets import packet_from_packet_stream

def parse_binary_packet_stream(fh):
    while True:
        pos = fh.tell()
        if len(fh.read(1)) != 1:
            return
        fh.seek(pos)
        packet = packet_from_packet_stream(fh)
        yield packet


def parse_binary_packet_data(data):
    offset = 0
    length = len(data)
    while offset < length:
        offset, packet = packet_from_packet_data(data, offset)
        yield packet


def parse_ascii_packet_data(data):
    armor = ASCIIArmor.from_ascii(data)
    return parse_binary_packet_data(bytes(armor))