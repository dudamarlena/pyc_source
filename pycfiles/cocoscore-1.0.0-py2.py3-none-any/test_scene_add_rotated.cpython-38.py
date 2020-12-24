# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\test\test_scene_add_rotated.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 1124 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, q'
tags = 'Scene, rotation'
import cocos
import cocos.director as director
from cocos.sprite import Sprite
from cocos.layer import *
import pyglet

class TestLayer(cocos.layer.Layer):

    def __init__(self):
        super(TestLayer, self).__init__()
        x, y = director.get_window_size()
        sprite1 = Sprite('grossini.png', (x // 4, y // 2))
        sprite2 = Sprite('grossinis_sister1.png', (x // 2, y // 2))
        sprite3 = Sprite('grossinis_sister2.png', (x / 1.3333333333333333, y // 2))
        self.add(sprite2)
        self.add(sprite1)
        self.add(sprite3)


def main():
    director.init()
    main_scene = cocos.scene.Scene()
    main_scene.add(ColorLayer(255, 0, 0, 255))
    l = TestLayer()
    l.rotation = 45
    main_scene.add(l)
    director.run(main_scene)


if __name__ == '__main__':
    main()