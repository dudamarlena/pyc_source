# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\cocos2020\test\test_anchors.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 1405 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 1, s, q'
tags = 'transform_anchor, scale, zoom'
import cocos
import cocos.director as director
from cocos.sprite import *
from cocos.layer import *
import pyglet

def main():
    director.init(resizable=True)
    main_scene = cocos.scene.Scene()
    white = ColorLayer(255, 255, 255, 255)
    red = ColorLayer(255, 0, 0, 255)
    blue = ColorLayer(0, 0, 255, 255)
    green = ColorLayer(0, 255, 0, 255)
    x, y = director.get_window_size()
    red.scale = 0.75
    blue.scale = 0.5
    blue.transform_anchor = (0, 0)
    green.scale = 0.25
    green.transform_anchor = (x, y)
    red.add((Sprite('grossini.png', (0, y // 2))), z=1)
    blue.add((Sprite('grossini.png', (0, y // 2))), z=1)
    green.add((Sprite('grossini.png', (0, y // 2))), z=1)
    red.add((Sprite('grossini.png', (x, y // 2))), z=1)
    blue.add((Sprite('grossini.png', (x, y // 2))), z=1)
    green.add((Sprite('grossini.png', (x, y // 2))), z=1)
    main_scene.add(white, z=0)
    main_scene.add(red, z=1)
    main_scene.add(blue, z=2)
    main_scene.add(green, z=3)
    director.run(main_scene)


if __name__ == '__main__':
    main()