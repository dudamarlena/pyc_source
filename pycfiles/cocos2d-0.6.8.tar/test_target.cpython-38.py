# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
    __doc__ = "\n    A CocosNode proxy that only offers the members a particular action needs\n    and prints to stdout the changes made for the action in those members.\n\n    Here is special cased to Rotate.\n\n    Notice that changes produced by the action don't reachs the cocosnode\n    "
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