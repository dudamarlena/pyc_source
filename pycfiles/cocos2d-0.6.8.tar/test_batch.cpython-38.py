# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\cocos2020\test\test_batch.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 1742 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, t 3.0, s, t 5.0, s, t 10.0, s, q'
tags = 'batch, BatchNode, Sprite'
import cocos
import cocos.director as director
from cocos.sprite import Sprite
import pyglet
from cocos.actions import MoveBy

class TestNoBatch(cocos.layer.Layer):

    def __init__(self):
        super(TestNoBatch, self).__init__()
        x, y = director.get_window_size()
        self.batch = cocos.cocosnode.CocosNode()
        self.batch.position = (50, 100)
        self.add(self.batch)
        for i in range(216):
            sprite = Sprite('grossini.png')
            sprite.position = (i // 12 * 30, i % 12 * 25)
            self.batch.add(sprite)
        else:
            self.batch.do(MoveBy((100, 100), 10))


class TestBatch(cocos.layer.Layer):

    def __init__(self):
        super(TestBatch, self).__init__()
        x, y = director.get_window_size()
        self.batchnode = cocos.batch.BatchNode()
        self.batchnode.position = (50, 100)
        self.add(self.batchnode)
        for i in range(216):
            sprite = Sprite('grossini.png')
            sprite.position = (i // 12 * 30, i % 12 * 25)
            self.batchnode.add(sprite)
        else:
            self.batchnode.do(MoveBy((100, 100), 10))


def main():
    director.init()
    test_layer = TestBatch()
    main_scene = cocos.scene.Scene(test_layer)
    director.show_FPS = True
    director.run(main_scene)


if __name__ == '__main__':
    main()