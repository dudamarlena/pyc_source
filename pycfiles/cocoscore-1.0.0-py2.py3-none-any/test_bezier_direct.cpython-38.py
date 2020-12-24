# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\test\test_bezier_direct.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 2216 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, t 2.0, s, t 3.0, s, t 5.0, s, q'
tags = 'Bezier, path'
import cocos
import cocos.director as director
from cocos.actions import Bezier
from cocos.sprite import Sprite
import pyglet
from cocos import path

def direct_bezier(p0, p1, p2, p3):
    """Given four points, returns a bezier path that go through them.

    It starts in p0, finish in p3, and pass through p1 and p2 in t=0.4 and
    t=0.6 respectively.
    """

    def _one_dim(p0xy, B1xy, B2xy, p3xy):
        """Calculates the p1 and p2 to draw through B1 and B2 given p0 and p3.

        p0: P sub 0 of bezier, it's also B(0)
        B1: B(0.4)
        B2: B(0.6)
        p3: P sub 3 of bezier, it's also B(1)
        """
        p2xy = (1.5 * B2xy - B1xy + 0.12 * p0xy - 0.26 * p3xy) / 0.36
        p1xy = (B2xy - 0.064 * p0xy - 0.432 * p2xy - 0.216 * p3xy) / 0.288
        return (
         p1xy, p2xy)

    bp1x, bp2x = _one_dim(p0[0], p1[0], p2[0], p3[0])
    bp1y, bp2y = _one_dim(p0[1], p1[1], p2[1], p3[1])
    bp1 = (
     bp1x, bp1y)
    bp2 = (bp2x, bp2y)
    bezier_path = path.Bezier(p0, p3, bp1, bp2)
    return bezier_path


class TestLayer(cocos.layer.Layer):

    def __init__(self):
        super(TestLayer, self).__init__()
        go_through = [
         (100, 300), (370, 330), (430, 270), (750, 550)]
        for pos in go_through:
            sprite = Sprite('fire.png')
            sprite.position = pos
            sprite.scale = 0.3
            self.add(sprite)

        bezier_path = direct_bezier(*go_through)
        sprite = Sprite('fire.png')
        sprite.scale = 0.3
        sprite.color = (0, 0, 255)
        self.add(sprite, z=5)
        sprite.do(Bezier(bezier_path, 5))


def main():
    director.init(width=800, height=600)
    test_layer = TestLayer()
    main_scene = cocos.scene.Scene(test_layer)
    director.run(main_scene)


if __name__ == '__main__':
    main()