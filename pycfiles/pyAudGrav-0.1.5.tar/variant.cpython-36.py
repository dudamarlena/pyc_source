# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/postlund/pyatv_dev/pyatv/pyatv/mrp/variant.py
# Compiled at: 2019-09-26 00:19:20
# Size of source mod 2**32: 585 bytes
__doc__ = 'Module to read and write Google protobuf variants.'

def read_variant(variant):
    """Read and parse a binary protobuf variant value."""
    result = 0
    cnt = 0
    for data in variant:
        result |= (data & 127) << 7 * cnt
        cnt += 1
        if not data & 128:
            return (result, variant[cnt:])

    raise Exception('invalid variant')


def write_variant(number):
    """Convert an integer to a protobuf variant binary buffer."""
    if number < 128:
        return bytes([number])
    else:
        return bytes([number & 127 | 128]) + write_variant(number >> 7)