# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\cocos2020\test\test_parallax.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 1642 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, t 1.1, s, t 2.1, s, t 3.1, s, q'
tags = 'parallax, set_focus, ScrollableLayer'
autotest = 0
import cocos
import cocos.director as director
from cocos.text import Label
from cocos.layer import ScrollingManager, ScrollableLayer
from pyglet.window import key
from cocos.actions import Delay, CallFunc

def update_focus(fx, fy):
    m.set_focus(fx, fy)


def main():
    global m
    director.init()
    m = ScrollingManager()
    fg = ScrollableLayer()
    l = Label('foreground')
    l.position = (100, 100)
    fg.add(l)
    m.add(fg)
    bg = ScrollableLayer(parallax=0.5)
    l = Label('background, parallax=.5')
    l.position = (100, 100)
    bg.add(l)
    m.add(bg)
    if autotest:
        m.do(Delay(1) + CallFunc(update_focus, 100, 200) + Delay(1) + CallFunc(update_focus, 200, 100) + Delay(1) + CallFunc(update_focus, 200, 200))
    main_scene = cocos.scene.Scene(m)
    keyboard = key.KeyStateHandler()
    director.window.push_handlers(keyboard)

    def update(dt):
        m.fx += (keyboard[key.RIGHT] - keyboard[key.LEFT]) * 150 * dt
        m.fy += (keyboard[key.DOWN] - keyboard[key.UP]) * 150 * dt
        m.set_focus(m.fx, m.fy)

    main_scene.schedule(update)
    director.run(main_scene)


if __name__ == '__main__':
    main()