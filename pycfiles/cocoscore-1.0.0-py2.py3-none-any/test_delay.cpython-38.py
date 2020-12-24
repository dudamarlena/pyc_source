# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\test\test_delay.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 1289 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, t 3, s, t 4.1, s, t 6, s, q'
tags = 'Delay, RandomDelay'
import cocos
import cocos.director as director
from cocos.actions import MoveBy, Delay, RandomDelay
from cocos.sprite import Sprite
import pyglet

class TestLayer(cocos.layer.Layer):

    def __init__(self):
        super(TestLayer, self).__init__()
        x, y = director.get_window_size()
        self.sprite = Sprite('grossini.png', (0, y // 2))
        self.add(self.sprite)
        self.sprite2 = Sprite('grossini.png', (0, y // 4))
        self.add(self.sprite2)
        self.sprite3 = Sprite('grossini.png', (0, y // 4 * 3))
        self.add(self.sprite3)
        self.sprite.do(Delay(2) + MoveBy((x, 0)))
        self.sprite2.do(RandomDelay(2, 4) + MoveBy((x, 0)))
        self.sprite3.do(RandomDelay(2, 4) + MoveBy((x, 0)))


def main():
    director.init()
    test_layer = TestLayer()
    main_scene = cocos.scene.Scene(test_layer)
    director.run(main_scene)


if __name__ == '__main__':
    main()