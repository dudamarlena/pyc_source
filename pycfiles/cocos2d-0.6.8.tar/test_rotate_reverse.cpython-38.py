# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\cocos2020\test\test_rotate_reverse.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 1670 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, t 1.1, s, t 3.1, s, t 4.1, s, q'
tags = 'RotateBy, Reverse'
autotest = 0
import pyglet, cocos
from cocos.actions import *
import cocos.director as director
key = pyglet.window.key

class DebugLabel(cocos.text.Label):

    def draw(self):
        sprite = self.parent.sprite
        self.element.text = '* (%.0f, %.0f) %.0f' % (sprite.position + (
         sprite.rotation,))
        super(DebugLabel, self).draw()


class Logo(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self):
        super(Logo, self).__init__()
        self.wx, self.wy = director.get_window_size()
        self.sprite = cocos.sprite.Sprite('grossini.png')
        self.sprite.position = (self.wx // 2, self.wy // 2)
        self.label = DebugLabel()
        self.add(self.label)
        self.add(self.sprite)
        self.schedule(lambda x: 0)
        if autotest:
            self.do(CallFunc(self.on_key_press, key.SPACE, 0))

    def on_key_press(self, k, m):
        if k == key.SPACE:
            action = RotateBy(180, 1.0) + Delay(1.0)
            self.sprite.do(action + Reverse(action))


def main():
    print('press space to initiate action')
    director.init(fullscreen=0, width=800, height=600)
    scene = cocos.scene.Scene()
    scene.add(Logo())
    director.run(scene)


if __name__ == '__main__':
    main()