# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\test\test_layeractions.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 817 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, t 2.5, s, t 5.1, s, q'
tags = 'MoveBy'
import cocos
import cocos.director as director
from cocos.sprite import Sprite
from cocos.actions import *
import pyglet

def main():
    director.init()
    bg_layer = cocos.layer.ColorLayer(255, 0, 0, 255)
    translate_layer = cocos.layer.Layer()
    x, y = director.get_window_size()
    translate_layer.add(bg_layer)
    translate_layer.do(MoveBy((x // 2, y // 2), 5))
    main_scene = cocos.scene.Scene(translate_layer)
    director.run(main_scene)


if __name__ == '__main__':
    main()