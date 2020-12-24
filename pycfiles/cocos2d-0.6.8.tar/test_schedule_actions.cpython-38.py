# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\cocos2020\test\test_schedule_actions.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 1010 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 'dt 0.1, q'
tags = 'actions'
import cocos
import cocos.director as director
from cocos.actions import *
from cocos.sprite import Sprite
import pyglet

class TestLayer(cocos.layer.Layer):

    def _step(self, dt):
        super(TestLayer, self)._step(dt)
        print('shall not happen')
        print(self.rotation)


description = '\nIf a node is not in the active scene, will not perfom any action.\nNo output should be seen on console.\n'

def main():
    print(description)
    director.init()
    test_layer = TestLayer()
    main_scene = cocos.scene.Scene()
    test_layer.do(RotateBy(360, duration=2))
    director.run(main_scene)


if __name__ == '__main__':
    main()