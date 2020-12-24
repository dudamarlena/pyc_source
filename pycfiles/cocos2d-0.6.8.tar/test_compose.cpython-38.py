# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\cocos2020\test\test_compose.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 1109 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, t 1.5, s, t 3, s, t 4.1, s, q'
tags = 'compose_actions, sequence, spawn'
import pyglet, cocos
from cocos.actions import ScaleTo, MoveTo, Accelerate
from cocos.sprite import Sprite
import cocos.director as director
from cocos.scene import Scene

class Bg(cocos.layer.Layer):

    def __init__(self):
        super(Bg, self).__init__()
        self.image = pyglet.resource.image('grossini.png')

    def on_enter(self):
        super(Bg, self).on_enter()
        sprite = Sprite(self.image)
        self.add(sprite)
        sprite.position = (320, 240)
        sprite.do(ScaleTo(4, 0))
        action = MoveTo((640, 480), 4) | ScaleTo(2, 2) + ScaleTo(4, 2)
        sprite.do(action)


def main():
    director.init()
    director.run(Scene(Bg()))


if __name__ == '__main__':
    main()