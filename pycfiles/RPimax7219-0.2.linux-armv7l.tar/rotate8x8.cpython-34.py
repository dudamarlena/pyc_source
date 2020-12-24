# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/RPimax7219/rotate8x8.py
# Compiled at: 2016-09-06 22:40:29
# Size of source mod 2**32: 1253 bytes


def _table(n):
    return [x << n for x in [
     0, 1, 256, 257,
     65536, 65537, 65792, 65793,
     16777216, 16777217, 16777472, 16777473,
     16842752, 16842753, 16843008, 16843009]]


ltab = [_table(i) for i in range(7, -1, -1)]

def rotate(src):
    """
    Rotate an 8x8 tile (8-element array of 8-bit numbers) 90 degrees
    counter-clockwise by table lookup. Large bitmaps can be rotated
    an 8x8 tile at a time. The extraction is done a nybble at a time
    to reduce the size of the tables.
    """
    assert len(src) == 8
    low = 0
    hi = 0
    for i in range(8):
        value = src[i]
        assert 0 <= value < 256, 'src[{0}] {1} outside range 0..255'.format(i, value)
        low |= ltab[i][(value & 15)]
        hi |= ltab[i][(value >> 4)]

    return [int(val >> i & 255) for val in [low, hi] for i in [0, 8, 16, 24]]