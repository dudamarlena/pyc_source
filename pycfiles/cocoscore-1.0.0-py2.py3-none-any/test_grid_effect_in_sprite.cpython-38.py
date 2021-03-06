# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\test\test_grid_effect_in_sprite.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 1935 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, t 1.7, s, t 3.7, s, t 6.7, s, t 9.7, s, t 12, s, q'
tags = 'Sprites, Waves, Twirl, WavesTiles3D, TurnOffTiles, StopGrid'
import cocos
import cocos.director as director
from cocos.sprite import Sprite
from cocos.actions import *
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


class TestLayer(cocos.layer.Layer):

    def __init__(self):
        super(TestLayer, self).__init__()
        x, y = director.get_window_size()
        self.sprite = Sprite('grossini.png', (x // 2, y // 2), scale=1)
        self.add(self.sprite)
        self.sprite.do(Repeat(ScaleBy(5, 2) + ScaleBy(0.2, 2)))
        self.sprite.do(Repeat(RotateBy(360, 10)))
        self.sprite.do(Waves(duration=3) + Twirl(amplitude=1, twirls=3, grid=(32, 24), duration=3) + WavesTiles3D(waves=4, grid=(32,
                                                                                                                                 24), duration=3) + TurnOffTiles(grid=(32,
                                                                                                                                                                       24), duration=1.5) + Reverse(TurnOffTiles(grid=(32,
                                                                                                                                                                                                                       24), duration=1.5)) + StopGrid())


def main():
    director.init()
    background = BackgroundLayer()
    test_layer = TestLayer()
    main_scene = cocos.scene.Scene()
    main_scene.add(background, z=0)
    main_scene.add(test_layer, z=1)
    director.run(main_scene)


if __name__ == '__main__':
    main()