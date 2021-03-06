# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\test\test_batch3.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 1554 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, t 3.0, s, t 5.0, s, t 10.0, s, q'
tags = 'batch, BatchNode.remove'
import cocos
import cocos.director as director
from cocos.sprite import Sprite
import pyglet
from cocos.actions import MoveBy

class TestBatch(cocos.layer.Layer):

    def __init__(self):
        super(TestBatch, self).__init__()
        x, y = director.get_window_size()
        self.batchnode = cocos.batch.BatchNode()
        self.batchnode.position = (50, 100)
        self.add(self.batchnode)
        for i in range(216):
            if i % 4 == 0:
                sprite = Sprite('grossini.png')
                self.parentSprite = sprite
                self.batchnode.add(sprite, z=(i % 4))
            else:
                sprite = Sprite('grossinis_sister1.png')
                self.parentSprite.add(sprite)
            sprite.position = (
             i // 12 * 30, i % 12 * 25)

        self.batchnode.remove(self.parentSprite)
        self.batchnode.do(MoveBy((100, 100), 10))


def main():
    director.init()
    test_layer = TestBatch()
    main_scene = cocos.scene.Scene(test_layer)
    director.show_FPS = True
    director.run(main_scene)


if __name__ == '__main__':
    main()