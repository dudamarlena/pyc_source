# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\cocos2020\test\test_world_coordinates.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 1573 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, t 2, s, t 5.1, s, q'
tags = 'point_to_world'
import cocos
import cocos.director as director
from cocos.sprite import Sprite
from cocos.actions import *
import pyglet
from pyglet.gl import *

class TestLayer(cocos.layer.Layer):

    def __init__(self):
        super(TestLayer, self).__init__()
        x, y = director.get_window_size()
        sprite1 = Sprite('grossini.png')
        self.add(sprite1)
        sprite1.position = (300, 300)
        sprite2 = Sprite('grossini.png')
        sprite1.add(sprite2)
        sprite2.position = (-50, -50)
        sprite3 = Sprite('grossini.png')
        sprite2.add(sprite3)
        sprite3.position = (150, 150)
        sprite3.rotation = 0
        sprite3.opacity = 128
        self.sprite3 = sprite3
        sprite1.do(ScaleBy(1.5, 10))
        sprite2.do(MoveBy((100, -150), 5))
        sprite3.do(RotateBy(360, 20))

    def draw(self):
        p = self.sprite3.point_to_world((0, 0))
        glPointSize(16)
        glBegin(GL_POINTS)
        glColor4f(1, 0, 0, 1)
        glVertex3f(p.x, p.y, 0)
        glEnd()


def main():
    director.init()
    test_layer = TestLayer()
    main_scene = cocos.scene.Scene(test_layer)
    director.run(main_scene)


if __name__ == '__main__':
    main()