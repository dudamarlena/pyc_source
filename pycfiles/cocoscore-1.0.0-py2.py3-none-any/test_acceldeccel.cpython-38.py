# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\test\test_acceldeccel.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 1314 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 1, s, t 2.0, s, t 4.1, s, q'
tags = 'AccelDeccel'
import cocos
import cocos.director as director
from cocos.actions import AccelDeccel, MoveBy, Reverse, Repeat
from cocos.sprite import Sprite
import pyglet

class TestLayer(cocos.layer.Layer):

    def __init__(self):
        super(TestLayer, self).__init__()
        x, y = director.get_window_size()
        self.sprite = Sprite('grossini.png', (0, y // 2))
        self.add(self.sprite)
        mov = AccelDeccel(MoveBy((x, 0), 4))
        self.sprite.do(Repeat(mov + Reverse(mov)))


description = '\nShows how to use AccelDeccel to modify an action by changing the time flow.\nAccelDeccel will reparametrize time for the target action.\nIt should be seen grossini moving between the left and right window border,\nmoving faster near the screen center.\n'

def main():
    print(description)
    director.init()
    test_layer = TestLayer()
    main_scene = cocos.scene.Scene(test_layer)
    director.run(main_scene)


if __name__ == '__main__':
    main()