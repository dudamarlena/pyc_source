# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/postlund/pyatv_dev/pyatv/pyatv/mrp/tlv8.py
# Compiled at: 2019-09-26 00:19:20
# Size of source mod 2**32: 1597 bytes
__doc__ = 'Implementation of TLV8 used by MRP/HomeKit pairing process.\n\nNote that this implementation only supports one level of value, i.e. no dicts\nin dicts.\n'
TLV_METHOD = '0'
TLV_IDENTIFIER = '1'
TLV_SALT = '2'
TLV_PUBLIC_KEY = '3'
TLV_PROOF = '4'
TLV_ENCRYPTED_DATA = '5'
TLV_SEQ_NO = '6'
TLV_BACK_OFF = '8'
TLV_SIGNATURE = '10'

def read_tlv(data):
    """Parse TLV8 bytes into a dict.

    If value is larger than 255 bytes, it is split up in multiple chunks. So
    the same tag might occurr several times.
    """

    def _parse(data, pos, size, result=None):
        if result is None:
            result = {}
        if pos >= size:
            return result
        else:
            tag = str(data[pos])
            length = data[(pos + 1)]
            value = data[pos + 2:pos + 2 + length]
            if tag in result:
                result[tag] += value
            else:
                result[tag] = value
            return _parse(data, pos + 2 + length, size, result)

    return _parse(data, 0, len(data))


def write_tlv(data):
    """Convert a dict to TLV8 bytes."""
    tlv = ''
    for key, value in data.items():
        tag = bytes([int(key)])
        length = len(value)
        pos = 0
        while pos < len(value):
            size = min(length, 255)
            tlv += tag
            tlv += bytes([size])
            tlv += value[pos:pos + size]
            pos += size
            length -= size

    return tlv