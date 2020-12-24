# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\cocos2020\test\test_camera_orbit_with_grid.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 1533 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import pyglet, cocos
import cocos.director as director
from cocos.actions import *
from cocos.layer import *
from pyglet.gl import *
testinfo = 't 0.1, s, t 3, s, t 6, s, t 8.1, s, q'
tags = 'OrbitCamera, reuse_grid'

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
    director.set_depth_test()
    main_scene = cocos.scene.Scene()
    main_scene.add((BackgroundLayer()), z=0)
    e = WavesTiles3D(amplitude=60, waves=4, grid=(32, 24), duration=4)
    rot = OrbitCamera(angle_x=45, angle_z=0, delta_z=360, duration=4)
    main_scene.do(e)
    main_scene.do(rot + Reverse(rot))
    director.run(main_scene)


if __name__ == '__main__':
    main()