# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\midi\util.py
# Compiled at: 2018-03-19 10:03:58
# Size of source mod 2**32: 983 bytes


def read_varlen(data):
    NEXTBYTE = 1
    value = 0
    while NEXTBYTE:
        chr = ord(bytearray([next(data)]))
        if not chr & 128:
            NEXTBYTE = 0
        chr = chr & 127
        value = value << 7
        value += chr

    return value


def write_varlen(value):
    chr1 = bytearray([value & 127])
    value >>= 7
    if value:
        chr2 = bytearray([value & 127 | 128])
        value >>= 7
        if value:
            chr3 = bytearray([value & 127 | 128])
            value >>= 7
            if value:
                chr4 = bytearray([value & 127 | 128])
                res = chr4 + chr3 + chr2 + chr1
            else:
                res = chr3 + chr2 + chr1
        else:
            res = chr2 + chr1
    else:
        res = chr1
    return res