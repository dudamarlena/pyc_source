# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/synth/midi/utils.py
# Compiled at: 2015-04-18 11:05:46
import binascii

def bytes_to_int(bytes):
    return int(binascii.b2a_hex(bytes), 16)


def parse_varbyte_as_int(fp, return_bytes_read=True):
    """Read a variable length of bytes from the file and return the
    corresponding integer."""
    result = 0
    bytes_read = 1
    result = bytes_to_int(fp.read(1))
    if result & 128:
        v = result
        result = result & 127
        while v & 128:
            v = bytes_to_int(fp.read(1))
            result = (result << 7) + (v & 127)
            bytes_read += 1

    return (
     result, bytes_read)