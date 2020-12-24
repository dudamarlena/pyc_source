# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\cocos2020\test\test_hierarchy2.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 2024 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, q'
tags = 'CocosNode, Sprite, child, rotation, position'
import cocos
import cocos.director as director
from cocos.sprite import Sprite
import pyglet

class TestLayer(cocos.layer.Layer):

    def __init__(self):
        super(TestLayer, self).__init__()
        x, y = director.get_window_size()
        self.sprite_a1 = Sprite('grossini.png', (x // 4, int(y * 0.66)))
        self.sprite_a2 = Sprite('grossini.png', (0, 0), rotation=30)
        self.sprite_a3 = Sprite('grossini.png', (0, 0), rotation=30)
        self.sprite_a1.add(self.sprite_a2)
        self.sprite_a2.add(self.sprite_a3)
        self.add(self.sprite_a1)
        self.sprite_b1 = Sprite('grossinis_sister1.png', (x // 2, int(y * 0.66)))
        self.sprite_b2 = Sprite('grossinis_sister1.png', (100, 0))
        self.sprite_b3 = Sprite('grossinis_sister1.png', (100, 0))
        self.sprite_b1.add(self.sprite_b2)
        self.sprite_b2.add(self.sprite_b3)
        self.add(self.sprite_b1)
        self.sprite_c1 = Sprite('grossinis_sister2.png', (int(x * 0.33), int(y * 0.33)))
        self.sprite_c2 = Sprite('grossinis_sister2.png', (100, 0), rotation=30)
        self.sprite_c3 = Sprite('grossinis_sister2.png', (100, 0), rotation=30)
        self.sprite_c1.add(self.sprite_c2)
        self.sprite_c2.add(self.sprite_c3)
        self.add(self.sprite_c1)


def main():
    director.init()
    test_layer = TestLayer()
    main_scene = cocos.scene.Scene(test_layer)
    director.run(main_scene)


if __name__ == '__main__':
    main()