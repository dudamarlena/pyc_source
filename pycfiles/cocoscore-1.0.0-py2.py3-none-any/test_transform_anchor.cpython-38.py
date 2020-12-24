# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\test\test_transform_anchor.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 3152 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, t 1.25, s, t 3, s, t 5, s, q'
tags = 'CocosNode, transform_anchor'
import cocos
import cocos.director as director
import cocos.actions as ac
from cocos.layer import *
description = '\nDemostrates:\n    CocosNode transform_anchor role (defines point to rotate around / zoom in\n    or out)\n\nYou should see:\n    Two squares performing the same action; they only differ in the\n    transform_anchor value\n\n    bluish square alternates between still, rotating around his own center,\n    zooming in and out with focus on his own center\n\n    redish square alternates between still, rotating around his bottom left\n    corner, zooming in and out with focus on his bottom left corner.\n'

def get_test_scene():
    template_action = ac.Repeat(ac.Delay(1.0) + ac.Rotate(360, 2.0) + ac.Delay(1.0) + ac.ScaleTo(2.0, 1.0) + ac.ScaleTo(1.0, 1.0))
    w, h = director.get_window_size()
    world = cocos.layer.Layer()
    bluish_square = cocos.layer.ColorLayer(0, 160, 176, 255, width=100, height=100)
    bluish_square.transform_anchor = (
     bluish_square.width / 2.0, bluish_square.height / 2.0)
    bluish_square.position = (w // 3, h // 2)
    bluish_square.do(template_action)
    world.add(bluish_square, z=2)
    mark_anchor = cocos.layer.ColorLayer(161, 191, 54, 255, width=8, height=8)
    mark_anchor.position = (bluish_square.x + bluish_square.transform_anchor_x,
     bluish_square.y + bluish_square.transform_anchor_y)
    world.add(mark_anchor, z=3)
    redish_square = cocos.layer.ColorLayer(201, 43, 0, 255, width=100, height=100)
    redish_square.transform_anchor = (0, 0)
    redish_square.position = (w * 2 // 3, h // 2)
    redish_square.do(template_action)
    world.add(redish_square, z=2)
    mark_anchor = cocos.layer.ColorLayer(161, 191, 54, 255, width=8, height=8)
    mark_anchor.position = (redish_square.x + redish_square.transform_anchor_x,
     redish_square.y + redish_square.transform_anchor_y)
    world.add(mark_anchor, z=3)
    scene = cocos.scene.Scene()
    scene.add(world)
    return scene


def main():
    print(description)
    director.init(resizable=True)
    scene = get_test_scene()
    director.run(scene)


if __name__ == '__main__':
    main()