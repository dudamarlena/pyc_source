# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Python35\Lib\site-packages\twistedlilypad\Utilities\DecoderUtilities.py
# Compiled at: 2015-01-14 16:07:39
# Size of source mod 2**32: 775 bytes
from codecs import getdecoder
from struct import unpack
uft8_decoder = getdecoder('UTF-8')

def varIntParser(data):
    return varIntParserWithLength(data)[:2]


def varIntParserWithLength(data):
    value = 0
    shift = 0
    byte = unpack('!B', data[shift])[0]
    while True:
        value |= (byte & 127) << shift * 7
        shift += 1
        if shift > 5:
            raise OverflowError('VarInt is too long')
        if byte & 128 == 0:
            break
        byte = unpack('!B', data[shift])[0]

    return (value, data[shift:], shift)


def varIntPrefixedStringParser(data):
    length, data = varIntParser(data)
    value = uft8_decoder(data[:length])[0]
    return (
     value, data[length:])