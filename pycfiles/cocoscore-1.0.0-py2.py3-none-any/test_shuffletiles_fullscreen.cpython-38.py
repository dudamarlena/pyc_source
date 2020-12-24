# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\test\test_shuffletiles_fullscreen.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 1675 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, t 0.49, s, t 0.51, s, t 2.49, s, t 2.51, s, t 2.99, s, t 3.1, s, q'
tags = 'CallFunc, Delay, fullscreen'
import pyglet, cocos
import cocos.director as director
import cocos.actions as ac
from cocos.layer import *
from pyglet import gl

class BackgroundLayer(cocos.layer.Layer):

    def __init__(self):
        super(BackgroundLayer, self).__init__()
        self.img = pyglet.resource.image('background_image.png')

    def draw(self):
        gl.glColor4ub(255, 255, 255, 255)
        gl.glPushMatrix()
        self.transform()
        self.img.blit(0, 0)
        gl.glPopMatrix()


def toggle_fullscreen():
    director.window.set_fullscreen(not director.window.fullscreen)


def main():
    director.init(resizable=True, fullscreen=False)
    main_scene = cocos.scene.Scene()
    main_scene.add((BackgroundLayer()), z=0)
    action1 = ac.ShuffleTiles(grid=(16, 8), seed=2, duration=3) + ac.StopGrid()
    action2 = ac.Delay(0.5) + ac.CallFunc(toggle_fullscreen) + ac.Delay(2.0) + ac.CallFunc(toggle_fullscreen)
    combo_action = action1 | action2
    main_scene.do(combo_action)
    director.run(main_scene)


if __name__ == '__main__':
    main()