# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\test\test_ripple3d.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 1254 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, t 0.3, s, t 0.5, s, t 1, s, q'
tags = 'Ripple3D'
import pyglet
from pyglet.gl import glColor4ub, glPushMatrix, glPopMatrix
import cocos
import cocos.director as director
from cocos.actions import *

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
    e = Ripple3D(radius=240, grid=(32, 24), duration=20, waves=20, amplitude=60)
    main_scene.do(e)
    director.run(main_scene)


if __name__ == '__main__':
    main()