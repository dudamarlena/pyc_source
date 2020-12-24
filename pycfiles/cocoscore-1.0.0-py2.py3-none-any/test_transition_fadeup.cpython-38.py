# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\test\test_transition_fadeup.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 1300 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, t 0.5, s, t 1, s, t 1.5, s, t 2.1, s, q'
tags = 'FadeUpTransition'
import cocos
import cocos.director as director
from cocos.actions import *
from cocos.layer import *
from cocos.scenes import *
from cocos.sprite import *
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
    scene1 = cocos.scene.Scene()
    scene2 = cocos.scene.Scene()
    colorl = ColorLayer(32, 32, 255, 255)
    sprite = Sprite('grossini.png', (320, 240))
    colorl.add(sprite)
    scene1.add((BackgroundLayer()), z=0)
    scene2.add(colorl, z=0)
    director.run(FadeUpTransition(scene1, 2, scene2))


if __name__ == '__main__':
    main()