# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\test\test_repeat2.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 1079 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, t 0.5, s, t 1, s, t 1.5, s, t 2, s, t 2.5, s, q'
tags = 'Repeat'
import cocos
import cocos.director as director
from cocos.actions import Repeat, Rotate, MoveBy, Place
from cocos.sprite import Sprite
import pyglet

class TestLayer(cocos.layer.Layer):

    def __init__(self):
        super(TestLayer, self).__init__()
        x, y = director.get_window_size()
        self.sprite = Sprite('grossini.png', (x // 2, y // 2))
        self.add(self.sprite)
        move = MoveBy((100, 0), 1)
        rot = Rotate(360, 1)
        seq = Place((x // 4, y // 2)) + rot + move
        self.sprite.do(Repeat(seq))


def main():
    director.init()
    test_layer = TestLayer()
    main_scene = cocos.scene.Scene(test_layer)
    director.run(main_scene)


if __name__ == '__main__':
    main()