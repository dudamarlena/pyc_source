# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\test\test_handler.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 932 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, q'
tags = 'is_event_handler, on_key_press'
import cocos
import cocos.director as director
from cocos.sprite import Sprite
import pyglet

class PrintKey(cocos.layer.Layer):
    is_event_handler = True

    def on_key_press(self, key, modifiers):
        print('Key Pressed:', key, modifiers)


description = '\nWhen pressing keys the key with modifiers should print on console\n'

def main():
    print(description)
    director.init()
    bg_layer = cocos.layer.ColorLayer(255, 0, 0, 255)
    test_layer = PrintKey()
    main_scene = cocos.scene.Scene(bg_layer, test_layer)
    director.run(main_scene)


if __name__ == '__main__':
    main()