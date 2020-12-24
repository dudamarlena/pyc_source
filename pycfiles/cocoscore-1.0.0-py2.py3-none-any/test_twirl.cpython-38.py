# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\test\test_twirl.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 1285 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, t 2, s, t 5.1, s, q'
tags = 'Twirl'
import cocos
import cocos.director as director
from cocos.actions import *
from cocos.layer import *
import pyglet
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
    main_scene.add((BackgroundLayer()), z=0)
    main_scene.do(Twirl(twirls=2, center=(320, 240), amplitude=1, grid=(32, 24),
      duration=5))
    director.run(main_scene)


if __name__ == '__main__':
    main()