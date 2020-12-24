# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\test\test_draw.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 1306 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, q'
tags = 'Canvas, line_to'
import cocos
import cocos.director as director
from cocos import draw
import pyglet, random
ri = random.randint

class TestFigure(draw.Canvas):

    def render(self):
        x, y = director.get_window_size()
        for i in range(100):
            start = (
             ri(0, 640), ri(0, 480))
            end = (ri(0, 640), ri(0, 480))
            color = (ri(0, 255), ri(0, 255), ri(0, 255), ri(0, 255))
            width = ri(1, 20)
            if random.random() < 0.3:
                self.set_color(color)
                self.set_stroke_width(width)
                self.move_to(start)
            self.line_to(end)


class TestLayer(cocos.layer.Layer):

    def __init__(self):
        super(TestLayer, self).__init__()
        self.add(TestFigure())
        self.schedule(lambda x: 0)


def main():
    director.init()
    test_layer = TestLayer()
    main_scene = cocos.scene.Scene(test_layer)
    director.run(main_scene)


if __name__ == '__main__':
    main()