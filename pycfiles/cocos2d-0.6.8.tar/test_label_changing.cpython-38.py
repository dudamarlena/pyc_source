# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\cocos2020\test\test_label_changing.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 1613 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, t 1.1, s, t 2.1, s, t 3.1, s, q'
tags = 'Label, color, text'
import cocos
import cocos.director as director
from cocos.sprite import Sprite
from cocos.actions import Rotate, Repeat, Delay, CallFunc
from cocos.text import Label

class TestLayer(cocos.layer.Layer):

    def __init__(self):
        super(TestLayer, self).__init__()
        x, y = director.get_window_size()
        self.color1 = [255, 0, 0, 255]
        self.color2 = [0, 0, 255, 255]
        self.label = Label('', (x // 2, y // 2))
        self.label.do(Rotate(360, 10))
        self.label.do(Repeat(Delay(1) + CallFunc(self.set_color, 0) + Delay(1) + CallFunc(self.set_color, 1) + Delay(1) + CallFunc(self.set_color, 2)))
        self.add(self.label)
        self.set_color(2)

    def set_color(self, color_selector):
        colors = [
         (255, 32, 64, 255), (0, 240, 100, 255), (90, 90, 250, 255)]
        color = colors[color_selector]
        text = '(%s, %s, %s, %s)' % color
        self.label.element.text = text
        self.label.element.color = color


def main():
    director.init()
    test_layer = TestLayer()
    main_scene = cocos.scene.Scene(test_layer)
    director.run(main_scene)


if __name__ == '__main__':
    main()