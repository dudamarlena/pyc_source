# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\test\test_unscaled_win_resize.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 1291 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, t 1, s, q'
tags = 'director.init, autoscale'
autotest = 0
import cocos
import cocos.director as director
from cocos.actions import MoveTo, Delay, CallFunc
from cocos.sprite import Sprite
import pyglet

class TestLayer(cocos.layer.Layer):

    def __init__(self):
        super(TestLayer, self).__init__()
        x, y = director.get_window_size()
        self.sprite = Sprite('grossini.png')
        self.add(self.sprite)
        self.sprite.do(MoveTo((x, y), 10))
        if autotest:
            self.do(Delay(1) + CallFunc(self.resize))

    def resize(self):
        director.window.set_size(600, 600)


description = '\nUsing autoscale=False in director.init, content will not\nbe scaled on resize. Use ctrl-f to toggle fullscreen\n'

def main():
    print(description)
    director.init(width=300, height=300, autoscale=False)
    test_layer = TestLayer()
    main_scene = cocos.scene.Scene(test_layer)
    director.run(main_scene)


if __name__ == '__main__':
    main()