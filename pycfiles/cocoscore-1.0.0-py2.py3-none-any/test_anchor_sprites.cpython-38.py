# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\test\test_anchor_sprites.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 2152 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, t 1.0, s, t 2.1, s, q'
tags = 'transform_anchor, Rotate'
import cocos
import cocos.director as director
from cocos.sprite import Sprite
from cocos.actions import *
import pyglet

class TestLayer(cocos.layer.Layer):

    def __init__(self):
        super(TestLayer, self).__init__()
        x, y = director.get_window_size()
        sprite1 = Sprite('grossini.png')
        sprite1.position = (x // 4, y // 2)
        self.add(sprite1)
        sprite2 = Sprite('grossini.png')
        sprite2.position = (x // 4, y // 2)
        self.add(sprite2, z=2)
        sprite2.scale = 0.3
        sprite2.do(RotateBy(duration=2, angle=360))
        sprite1.do(RotateBy(duration=2, angle=(-360)))
        sprite1.transform_anchor = (0, 0)
        sprite3 = Sprite('grossini.png')
        sprite3.position = (3 * x // 4, y // 2)
        self.add(sprite3)
        sprite4 = Sprite('grossini.png')
        sprite4.position = (3 * x // 4, y // 2)
        self.add(sprite4, z=2)
        sprite4.scale = 0.3
        sprite3.do(RotateBy(duration=2, angle=360))
        sprite4.do(RotateBy(duration=2, angle=(-360)))
        sprite3.transform_anchor = (
         sprite3.image.width // 2, sprite3.image.height // 2)


description = "\nShowing how CocosNode.transform_anchor affects rotation.\nAt the start\n    two grossinis will be seen on the left, the small one centered on\nthe center of the big one\n    two grossinis will be seen on the righ, the small one centered on\nthe center of of the big one\nThen all grossinis will rotate around it transform_anchor, so the two on\nthe left around it's center and the big one in the right around its\ntop-right corner.\n"

def main():
    print(description)
    director.init()
    test_layer = TestLayer()
    main_scene = cocos.scene.Scene(test_layer)
    director.run(main_scene)


if __name__ == '__main__':
    main()