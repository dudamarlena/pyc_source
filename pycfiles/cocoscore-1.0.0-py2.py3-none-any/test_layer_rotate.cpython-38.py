# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\test\test_layer_rotate.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 732 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, t 0.5, s, t 1.5, s, t 2.1, s, q'
tags = 'Layer, RotateBy'
import cocos
import cocos.director as director
from cocos.actions import RotateBy
from cocos.layer import *

def main():
    director.init()
    main_scene = cocos.scene.Scene()
    test_layer = ColorLayer(64, 64, 64, 255)
    test_layer.scale = 0.75
    main_scene.add(test_layer)
    test_layer.do(RotateBy(360, 2))
    director.run(main_scene)


if __name__ == '__main__':
    main()