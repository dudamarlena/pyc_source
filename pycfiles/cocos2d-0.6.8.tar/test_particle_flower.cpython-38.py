# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\cocos2020\test\test_particle_flower.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 1022 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 'f 10 0.033, s, f 20 0.033, s, f 30 0.033, s, f 30 0.033, s, q'
tags = 'particles, Flower'
import pyglet, cocos
import cocos.director as director
from cocos.actions import *
from cocos.layer import *
from cocos.particle_systems import *

class L(Layer):

    def __init__(self):
        super(L, self).__init__()
        p = Flower()
        p.position = (320, 240)
        self.add(p)


def main():
    director.init(resizable=True)
    main_scene = cocos.scene.Scene()
    main_scene.add(L())
    director.run(main_scene)


if __name__ == '__main__':
    main()