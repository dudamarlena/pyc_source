# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\cocos2020\test\test_fadein.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 951 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, t 2.5, s, t 5.1, s, t 5.2, s, q'
tags = 'FadeIn, opacity'
import cocos
import cocos.director as director
from cocos.actions import FadeIn
from cocos.sprite import Sprite

class TestLayer(cocos.layer.Layer):

    def __init__(self):
        super(TestLayer, self).__init__()
        x, y = director.get_window_size()
        self.sprite = Sprite('grossini.png', (x // 2, y // 2))
        self.sprite.opacity = 0
        self.add(self.sprite)
        self.sprite.do(FadeIn(5))


def main():
    director.init()
    test_layer = TestLayer()
    main_scene = cocos.scene.Scene(test_layer)
    director.run(main_scene)


if __name__ == '__main__':
    main()