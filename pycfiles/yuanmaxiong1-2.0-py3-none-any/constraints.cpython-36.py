# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\研发资料\瓦力课程\试听课\代码\dianyi\constraints.py
# Compiled at: 2019-08-09 00:27:00
# Size of source mod 2**32: 605 bytes
from .config import *

class Spring:

    def __init__(self):
        pass


class Connect(pymunk.constraint.PinJoint):

    def __init__(self, a, b):
        pymunk.constraint.PinJoint.__init__(a._gameObject.body.body, b._gameObject.body.body, (0,
                                                                                               0), (0,
                                                                                                    0))
        global_var.SPACE.add(self)


def connect(a, b):
    for vertice1 in a.vertices:
        for vertice2 in b.vertices:
            global_var.SPACE.add(pymunk.constraint.GearJoint(a.body, b.body, 0, 1))