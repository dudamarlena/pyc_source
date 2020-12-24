# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\cocos2020\test\test_scalexy.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 1785 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, q'
tags = 'Sprite, scale_x, scale_y'
import cocos
import cocos.director as director
from cocos.sprite import Sprite
import pyglet

class TestLayer(cocos.layer.Layer):

    def __init__(self):
        super(TestLayer, self).__init__()
        x, y = director.get_window_size()
        sprite = Sprite('grossini.png')
        sprite.position = (x // 5, y // 2)
        self.add(sprite)
        sprite = Sprite('grossini.png')
        sprite.position = (x * 2 // 5, y // 2)
        sprite.scale_x = 0.5
        self.add(sprite)
        sprite = Sprite('grossini.png')
        sprite.position = (x * 3 // 5, y // 2)
        sprite.scale_y = 0.5
        self.add(sprite)
        sprite = Sprite('grossini.png')
        sprite.position = (x * 4 // 5, y // 2)
        sprite.scale_y = 0.5
        sprite.scale = 2.0
        self.add(sprite)


description = '\nShows four images of Grossini, from left to right:\n    No scaled at all\n    scale_x = 0.5 , should look stretched to half width\n    scale_y = 0.5 , should look stretched to half height\n    scale_y = 0.5 and scale = 2.0 , should look normal height and double width\n'

def main():
    print(description)
    director.init()
    test_layer = TestLayer()
    main_scene = cocos.scene.Scene(test_layer)
    director.run(main_scene)


if __name__ == '__main__':
    main()