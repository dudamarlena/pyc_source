# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/layout/geometry/rotation.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 546 bytes
from enum import IntEnum

def rotate_and_flip(coord_map, rotation, flip):
    rotation = -rotation % 360 // 90
    for i in range(rotation):
        coord_map = list(zip(*coord_map[::-1]))

    if flip:
        coord_map = coord_map[::-1]
    return coord_map


from ...util import deprecated
if deprecated.allowed():

    class Rotation(IntEnum):
        ROTATE_0 = 0
        ROTATE_90 = 90
        ROTATE_180 = 180
        ROTATE_270 = 270