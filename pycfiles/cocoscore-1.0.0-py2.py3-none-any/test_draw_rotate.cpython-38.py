# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\test\test_draw_rotate.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 1288 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, q'
tags = 'Draw, Canvas.rotate'
import cocos
import cocos.director as director
from cocos import draw
import pyglet, math

class TestFigure(draw.Canvas):

    def render(self):
        x, y = director.get_window_size()
        ye = 50
        xs = 50
        line_width = 20
        self.set_color((255, 255, 0, 125))
        self.set_stroke_width(line_width)
        parts = 20
        self.set_endcap(draw.ROUND_CAP)
        self.translate((x // 2, y // 2))
        for i in range(parts):
            self.move_to((0, 0))
            self.line_to((xs, ye))
            self.rotate(2 * math.pi / parts)


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