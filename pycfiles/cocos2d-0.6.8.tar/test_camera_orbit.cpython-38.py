# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\cocos2020\test\test_camera_orbit.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 1670 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, t 2, s, t 4, s, t 6, s, t 8, s, t 10, s, t 12, s, t 14, s, t 16.1, s, q'
tags = 'OrbitCamera'
import pyglet, cocos
import cocos.director as director
from cocos.actions import *
from cocos.layer import *
from pyglet.gl import *

class BackgroundLayer(cocos.layer.Layer):

    def __init__(self):
        super(BackgroundLayer, self).__init__()
        self.img = pyglet.resource.image('background_image.png')

    def draw(self):
        glColor4ub(255, 255, 255, 255)
        glPushMatrix()
        self.transform()
        self.img.blit(0, 0)
        glPopMatrix()


def main():
    director.init(resizable=True)
    main_scene = cocos.scene.Scene()
    background = BackgroundLayer()
    color = ColorLayer(255, 32, 32, 128)
    main_scene.add(background, z=0)
    main_scene.add(color, z=1)
    rot = OrbitCamera(angle_x=45, angle_z=0, delta_z=360, duration=8)
    rot2 = OrbitCamera(radius=2, delta_radius=(-1), angle_x=0, angle_z=0, delta_z=360, duration=8)
    background.do(rot + Reverse(rot))
    color.do(rot2 + Reverse(rot2))
    director.run(main_scene)


if __name__ == '__main__':
    main()