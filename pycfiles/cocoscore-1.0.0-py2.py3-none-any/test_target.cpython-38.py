# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\test\test_target.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 1637 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 'dt 0.1, q'
tags = 'debugging'
import cocos
import cocos.director as director
from cocos.sprite import Sprite
from cocos.actions import *
import pyglet

class Dummy:
    """Dummy"""
    rotation = 0

    def __setattr__(self, attr, value):
        print('set', attr, 'to', value)


class TestLayer(cocos.layer.Layer):

    def __init__(self):
        super(TestLayer, self).__init__()
        x, y = director.get_window_size()
        self.sprite = Sprite('grossini.png')
        self.sprite.position = (x // 2, y // 2)
        self.add(self.sprite)
        self.sprite.do(Rotate(90, 3), Dummy())


description = '\nShows in the console the changes in a CocosNode instance produced by the a\nRotate action.\n\nThe node (grossini sprite) does not rotate on screen as a side effect of\nthe interception.\n\nVariants of this could come handy for debugging, testing. \n'

def main():
    print(description)
    director.init()
    test_layer = TestLayer()
    main_scene = cocos.scene.Scene(test_layer)
    director.run(main_scene)


if __name__ == '__main__':
    main()