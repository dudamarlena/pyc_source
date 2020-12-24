# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\cocos2020\test\test_sprite_aabb.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 2849 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, t 0.5, s, t 1, s, t 1.5, s, q'
tags = 'Sprite, bounding box'
import cocos
import cocos.director as director
from cocos.sprite import Sprite
from cocos.actions import *
import pyglet
from pyglet.gl import *
import cocos.euclid

class TestLayer(cocos.layer.Layer):

    def __init__(self):
        super(TestLayer, self).__init__()
        x, y = director.get_window_size()
        parent = Sprite('grossinis_sister1.png')
        self.add(parent)
        parent.position = (x // 2, y // 2)
        sprite = Sprite('grossinis_sister2.png')
        sprite.position = (100, 140)
        sprite.do(RotateBy(duration=2, angle=360))
        sprite.do(ScaleBy(duration=2, scale=2))
        sprite.do(MoveBy(duration=2, delta=(200, 0)))
        parent.add(sprite)
        sprite.opacity = 128
        self.sprite1 = sprite
        sprite = Sprite('grossini.png')
        self.add(sprite)
        sprite.position = (100, 140)
        sprite.do(RotateBy(duration=2, angle=360))
        sprite.do(ScaleBy(duration=2, scale=2))
        sprite.do(MoveBy(duration=2, delta=(200, 0)))
        self.sprite2 = sprite

    def draw(self):
        r = self.sprite2.get_AABB()
        left, bottom = r.left, r.bottom
        right, top = r.right, r.top
        glBegin(GL_LINE_LOOP)
        glColor4f(1, 0, 0, 1)
        glVertex3f(left, bottom, 0)
        glVertex3f(right, bottom, 0)
        glVertex3f(right, top, 0)
        glVertex3f(left, top, 0)
        glEnd()
        bl = self.sprite1.point_to_world((0, 0))
        x, y = self.sprite1.width, self.sprite2.height
        tr = self.sprite1.point_to_world((x, y))
        left, bottom = bl.x, bl.y
        right, top = tr.x, tr.y
        bl = self.sprite1.point_to_world((0, 0))
        glPointSize(16)
        glBegin(GL_POINTS)
        glColor4f(1, 1, 0, 1)
        glVertex3f(bl.x, bl.y, 0)
        glEnd()


def main():
    director.init()
    test_layer = TestLayer()
    main_scene = cocos.scene.Scene(test_layer)
    director.run(main_scene)


if __name__ == '__main__':
    main()