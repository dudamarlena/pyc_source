# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\cocos2020\test\test_accelerate_speed.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 1455 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 1, s, t 2, s, t 5, s, t 8, s, t 10.1, s, q'
tags = 'Speed, Accelerate'
import cocos
import cocos.director as director
from cocos.actions import Accelerate, Speed, Rotate
from cocos.sprite import Sprite
import pyglet

class TestLayer(cocos.layer.Layer):

    def __init__(self):
        super(TestLayer, self).__init__()
        x, y = director.get_window_size()
        self.sprite1 = Sprite('grossini.png', (x // 4, y // 2))
        self.add(self.sprite1)
        self.sprite2 = Sprite('grossini.png', (x // 4 * 3, y // 2))
        self.add(self.sprite2)
        self.sprite1.do(Accelerate(Speed(Rotate(360, 1), 0.1), 4))
        self.sprite2.do(Speed(Accelerate(Rotate(360, 1), 4), 0.1))


description = '\nShows how to use Speed to modify an action duration.\nSpeed will multiply by a factor the duration of the target action.\nIt should be seen two grossinis, rotating 360 degrees, first slowly\nthen faster. \n'

def main():
    print(description)
    director.init()
    test_layer = TestLayer()
    main_scene = cocos.scene.Scene()
    main_scene.add(test_layer)
    director.run(main_scene)


if __name__ == '__main__':
    main()