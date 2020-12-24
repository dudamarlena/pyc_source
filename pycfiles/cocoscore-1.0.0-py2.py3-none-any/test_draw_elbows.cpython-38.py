# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\test\test_draw_elbows.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 1651 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, q'
tags = 'Draw, join'
import cocos
import cocos.director as director
from cocos import draw
import pyglet

class TestFigure(draw.Canvas):

    def render(self):
        x, y = director.get_window_size()
        ys = y // 4
        ye = ys * 3
        xs = x // 4
        line_width = 50
        self.set_color((255, 255, 0, 100))
        self.set_stroke_width(line_width)
        self.set_join(draw.BEVEL_JOIN)
        self.move_to((xs + 100, ys))
        self.line_to((xs * 2 + 100, ys))
        self.line_to((xs * 2 + 100, ys * 2))
        self.line_to((xs * 3 + 100, ys * 2))
        self.set_join(draw.MITER_JOIN)
        self.move_to((xs, ys + 100))
        self.line_to((xs * 2, ys + 100))
        self.line_to((xs * 2, ys * 2 + 100))
        self.line_to((xs * 3, ys * 2 + 100))
        self.set_join(draw.ROUND_JOIN)
        self.move_to((xs - 100, ys + 200))
        self.line_to((xs * 2 - 100, ys + 200))
        self.line_to((xs * 2 - 100, ys * 2 + 200))
        self.line_to((xs * 3 - 100, ys * 2 + 200))


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