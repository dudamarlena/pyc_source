# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\test\test_tmxobjectlayer.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 1688 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, q'
tags = 'TMX, tiles, TmxObjectLayer'
import pyglet
from pyglet.window import key
from pyglet.gl import glClearColor
pyglet.resource.path.append(pyglet.resource.get_script_home())
pyglet.resource.reindex()
import cocos
from cocos import tiles, actions, layer
description = "\nLoads a tmx map containing a tile layer and an object layer.\nThe tiles layer is rendered as black region with four green dots.\n\nThe debug view of the TmxObjectLayer is draw over that, with four objects\nof type 'rect', 'ellipse', 'polygon', 'polyline'\n\nThe debug view only draws the Axis Aligned Bounding Box of each object.\n\nYou should see four green points covered by translucid white-ish rectangles,\nroughly centered at each point. \n"

def main():
    import cocos.director as director
    director.init(width=800, height=600, autoscale=False, resizable=True)
    glClearColor(255, 255, 255, 255)
    scroller = layer.ScrollingManager()
    maploaded = tiles.load('obj.tmx')
    test_layer = maploaded['tiles_layer_1']
    scroller.add(test_layer)
    object_layer = maploaded['test_object_layer']
    scroller.add(object_layer)
    main_scene = cocos.scene.Scene(scroller)
    print(test_layer.px_width, test_layer.px_height)
    scroller.set_focus(test_layer.px_width // 2, test_layer.px_height // 2)
    director.run(main_scene)


if __name__ == '__main__':
    print(description)
    main()