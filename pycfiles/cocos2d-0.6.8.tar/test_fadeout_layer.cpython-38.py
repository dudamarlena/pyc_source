# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\cocos2020\test\test_fadeout_layer.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 937 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, t 1, s, t 2, s, t 3, s, t 4.1, s, t 4.2, s, q'
tags = 'FadeIn, FadeOut, ColorLayer'
import pyglet
from pyglet.gl import *
import cocos
import cocos.director as director
from cocos.actions import *
from cocos.layer import *

def main():
    print(description)
    director.init(resizable=True)
    main_scene = cocos.scene.Scene()
    l = ColorLayer(255, 128, 64, 64)
    main_scene.add(l, z=0)
    l.do(FadeOut(duration=2) + FadeIn(duration=2))
    director.run(main_scene)


description = '\nA ColorLayer is faded-out and fadded-in.\nNotice this will not work for arbitrary Layer objects.\n'
if __name__ == '__main__':
    main()