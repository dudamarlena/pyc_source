# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/dustmaker/Prop.py
# Compiled at: 2015-10-28 00:08:06
# Size of source mod 2**32: 692 bytes
import math

class Prop:

    def __init__(self, layer_sub, rotation, scale_x, scale_y, prop_set, prop_group, prop_index, palette):
        self.layer_sub = layer_sub
        self.rotation = rotation
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.prop_set = prop_set
        self.prop_group = prop_group
        self.prop_index = prop_index
        self.palette = palette

    def transform(self, mat):
        angle = math.atan2(mat[1][1], mat[1][0]) - math.pi / 2
        self.rotation = self.rotation - int(65536 * angle / math.pi / 2) & 65535
        if mat[0][0] * mat[1][1] - mat[0][1] * mat[1][0] < 0:
            self.scale_x = not self.scale_x
            self.rotation = -self.rotation & 65535