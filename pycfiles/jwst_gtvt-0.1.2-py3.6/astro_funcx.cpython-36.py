# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/jwst_gtvt/astro_funcx.py
# Compiled at: 2020-02-10 11:10:52
# Size of source mod 2**32: 1216 bytes
from math import *
D2R = pi / 180.0
R2D = 180.0 / pi
PI2 = 2.0 * pi
epsilon = 23.43929 * D2R
unit_limit = lambda x: min(max(-1.0, x), 1.0)

def pa(tgt_c1, tgt_c2, obj_c1, obj_c2):
    """calculates position angle of object at tgt position."""
    y = cos(obj_c2) * sin(obj_c1 - tgt_c1)
    x = sin(obj_c2) * cos(tgt_c2) - cos(obj_c2) * sin(tgt_c2) * cos(obj_c1 - tgt_c1)
    p = atan2(y, x)
    if p < 0.0:
        p += PI2
    if p >= PI2:
        p -= PI2
    return p


def delta_pa_no_roll(pos1_c1, pos1_c2, pos2_c1, pos2_c2):
    """Calculates the change in position angle between two positions with no roll about V1"""
    u = (sin(pos1_c2) + sin(pos2_c2)) * sin(pos2_c1 - pos1_c1)
    v = cos(pos2_c1 - pos1_c1) + cos(pos1_c2) * cos(pos2_c2) + sin(pos1_c2) * sin(pos2_c2) * cos(pos2_c1 - pos1_c1)
    return atan2(u, v)


def dist(obj1_c1, obj1_c2, obj2_c1, obj2_c2):
    """angular distance betrween two objects, positions specified in spherical coordinates."""
    x = cos(obj2_c2) * cos(obj1_c2) * cos(obj2_c1 - obj1_c1) + sin(obj2_c2) * sin(obj1_c2)
    return acos(unit_limit(x))