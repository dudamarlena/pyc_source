# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\cocos2020\test\test_sceneactions.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 916 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, t 1, s, t 1.9, s, t 2.1, s, q'
tags = 'transform_anchor, scale'
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
    sub = cocos.scene.Scene(bg_layer)
    sub.transform_anchor = (0, 0)
    sub.scale = 0.5
    sub.do(MoveBy((x // 2, y // 2), 2))
    sub.do(ScaleBy(0.5, 2))
    main_scene = cocos.scene.Scene(sub)
    director.run(main_scene)


if __name__ == '__main__':
    main()