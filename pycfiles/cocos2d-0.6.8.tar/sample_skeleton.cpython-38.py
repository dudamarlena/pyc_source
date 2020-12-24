# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\cocos2020\test\sample_skeleton.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 926 bytes
from __future__ import division, print_function, unicode_literals
from cocos.skeleton import Bone, Skeleton

def Point2(*args):
    return args


root_bone = Bone('torso', 70, -180.0, Point2(0.0, 0.0)).add(Bone('brazo der', 40, 152.308491558, Point2(34.0, -67.0)).add(Bone('antebrazo der', 40, 121.203546669, Point2(-4.0, -36.0)))).add(Bone('brazo izq', 40, 222.115898576, Point2(-10.0, -70.0)).add(Bone('antebrazo izq', 40, 123.385130709, Point2(3.0, -47.0)))).add(Bone('muslo izq', 40, 225.0, Point2(-10.0, 5.0)).add(Bone('pierna izq', 40, -60.5241109968, Point2(3.0, -44.0)))).add(Bone('muslo der', 40, 179.587915727, Point2(18.0, 5.0)).add(Bone('pierna der', 40, -31.2908540886, Point2(4.0, -47.0)))).add(Bone('cabeza', 20, -9.90592089762, Point2(2.0, -94.0)))
skeleton = Skeleton(root_bone)