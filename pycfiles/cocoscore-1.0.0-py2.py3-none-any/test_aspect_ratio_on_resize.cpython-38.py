# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\test\test_aspect_ratio_on_resize.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 2732 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 's, q'
tags = 'aspect ratio, resize'
from pyglet.gl import *
import cocos
import cocos.director as director
from cocos.actions import Delay, CallFunc, Repeat
w_ini = 640
h_ini = 480
assert abs(w_ini / h_ini - 1.3333333333333333) < 0.0001

class ProbeRect(cocos.cocosnode.CocosNode):

    def __init__(self, w_ini, h_ini, color4):
        super(ProbeRect, self).__init__()
        self.color4 = color4
        w2 = int(w_ini // 2)
        h2 = int(h_ini // 2)
        self.vertexes = [(0, 0, 0), (0, h_ini, 0), (w_ini, h_ini, 0), (w_ini, 0, 0)]

    def draw(self):
        glPushMatrix()
        self.transform()
        glBegin(GL_QUADS)
        glColor4ub(*self.color4)
        for v in self.vertexes:
            glVertex3i(*v)

        glEnd()
        glPopMatrix()


class TestLayer(cocos.layer.Layer):

    def __init__(self):
        super(TestLayer, self).__init__()
        self.add((ProbeRect(w_ini, h_ini, (0, 0, 255, 255))), z=1)
        border_size = 10
        inner = ProbeRect(w_ini - 2 * border_size, h_ini - 2 * border_size, (255, 0,
                                                                             0, 255))
        inner.position = (border_size, border_size)
        self.add(inner, z=2)
        outer = ProbeRect(w_ini + 2 * border_size, h_ini + 2 * border_size, (255, 255,
                                                                             0, 255))
        outer.position = (-border_size, -border_size)
        self.add(outer, z=0)
        self.size_from_stage = [(800, 600), (800, 640),
         (840, 600), (w_ini, h_ini)]
        self.stage = 0
        self.do(Repeat(Delay(4) + CallFunc(self.rotate_sizes)))

    def rotate_sizes(self):
        (director.window.set_size)(*self.size_from_stage[self.stage])
        self.stage = (self.stage + 1) % len(self.size_from_stage)


description = '\nStarts a 4/3 aspect ratio window, and later resizes to diferent resolutions,\nnot always with 4:3 apect ratio.\n\nThe scene is composed by three rectangles centered at the window center:\n\n    blue   : the exact same size as the window\n    yellow : a little bigger than blue box\n    red    : a little smaller than blue box\n\nDraw order is yellow, blue, red.\n\nAt any resolution you must see no yellow, and a red rectangle with equal\nsized blue borders.\n\nWhen the aspect ratio is not 4:3, padding borders in black can be seen. \n'

def main():
    print(description)
    director.init(width=w_ini, height=h_ini, resizable=False)
    scene = cocos.scene.Scene()
    scene.add(TestLayer())
    director.run(scene)


if __name__ == '__main__':
    main()