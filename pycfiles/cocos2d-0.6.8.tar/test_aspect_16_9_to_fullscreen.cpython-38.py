# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\cocos2020\test\test_aspect_16_9_to_fullscreen.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 2339 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, q'
tags = 'resize, resizable, aspect ratio, set_caption'
from pyglet.gl import *
import cocos
import cocos.director as director
width = 768
height = 480
assert abs(width / height - 1.6) < 0.0001

class ProbeRect(cocos.cocosnode.CocosNode):

    def __init__(self, width, height, color4):
        super(ProbeRect, self).__init__()
        self.color4 = color4
        w2 = int(width // 2)
        h2 = int(height // 2)
        self.vertexes = [
         (0, 0, 0), (0, height, 0), (width, height, 0), (width, 0, 0)]

    def draw(self):
        glPushMatrix()
        self.transform()
        glBegin(GL_QUADS)
        glColor4ub(*self.color4)
        for v in self.vertexes:
            glVertex3i(*v)
        else:
            glEnd()
            glPopMatrix()


class TestLayer(cocos.layer.Layer):

    def __init__(self):
        super(TestLayer, self).__init__()
        self.add((ProbeRect(width, height, (0, 0, 255, 255))), z=1)
        border_size = 10
        inner = ProbeRect(width - 2 * border_size, height - 2 * border_size, (255,
                                                                              0,
                                                                              0,
                                                                              255))
        inner.position = (border_size, border_size)
        self.add(inner, z=2)
        outer = ProbeRect(width + 2 * border_size, height + 2 * border_size, (255,
                                                                              255,
                                                                              0,
                                                                              255))
        outer.position = (-border_size, -border_size)
        self.add(outer, z=0)


description = '\nStarts a 16/10 aspect ratio window.\nCTRL-F toggles fullscreen\n\nThe scene draw three boxes, centered at the window center.\n  blue box: the exact same size as the window\n  yellow box: a little bigger than blue box\n  red box: a little smaller than blue box\nDraw order is yellow, blue, red\nYou must see no yellow, and a red rectangle with equal sized blue borders\n'

def main():
    print(description)
    director.init(width=width, height=height, resizable=False)
    director.window.set_caption('aspect ratio and fullscreen - see console for usage')
    scene = cocos.scene.Scene()
    scene.add(TestLayer())
    director.run(scene)


if __name__ == '__main__':
    main()