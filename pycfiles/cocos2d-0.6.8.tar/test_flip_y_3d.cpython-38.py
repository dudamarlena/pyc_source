# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\cocos2020\test\test_flip_y_3d.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 1270 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, t 1, s, t 2, s, t 3, s, t 4.1, s, t 4.2, s, q'
tags = 'FlipY3D'
import pyglet
from pyglet.gl import glColor4ub, glPushMatrix, glPopMatrix
import cocos
import cocos.director as director
from cocos.actions import *
from cocos.sprite import *

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
    main_scene.add((BackgroundLayer()), z=0)
    main_scene.do(FlipY3D(duration=4))
    director.run(main_scene)


if __name__ == '__main__':
    main()