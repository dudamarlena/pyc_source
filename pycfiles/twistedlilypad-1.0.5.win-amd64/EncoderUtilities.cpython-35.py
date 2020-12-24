# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Python35\Lib\site-packages\twistedlilypad\Utilities\EncoderUtilities.py
# Compiled at: 2015-02-03 19:24:47
# Size of source mod 2**32: 666 bytes
from codecs import getencoder
from struct import pack
uft8_encoder = getencoder('UTF_8')

def varIntEncoder(number):
    result = []
    while number >= 128:
        result.append(pack('>B', number & 127 | 128))
        number >>= 7

    result.append(pack('>B', number))
    return ''.join(result)


def varIntPrefixedStringEncoder(string):
    encoded_string = uft8_encoder(string)[0]
    return varIntEncoder(len(encoded_string)) + encoded_string


def varIntPrefixedStringListEncoder(string_list):
    return ''.join(varIntPrefixedStringEncoder(string) for string in string_list)


def booleanEncoder(boolean):
    return pack('>B', 1 if boolean else 0)