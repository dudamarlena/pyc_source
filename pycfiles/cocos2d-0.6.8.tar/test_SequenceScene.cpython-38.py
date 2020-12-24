# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\cocos2020\test\test_SequenceScene.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 1565 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, t 2.1, s, t 4.1, s, t 6.1, s, q'
tags = 'SequenceScene, CallFunc'
import cocos.director as director
from cocos.scene import Scene
from cocos.scenes.sequences import SequenceScene
from cocos.layer import *
import cocos.actions as ac

def pop_scene():
    director.pop()


def push_sequence_scene():
    scene_blue = Scene()
    layer_blue = ColorLayer(32, 32, 255, 255)
    scene_blue.add(layer_blue, z=0)
    scene_blue.do(ac.Delay(2) + ac.CallFunc(pop_scene))
    scene_red = Scene()
    layer_red = ColorLayer(255, 32, 0, 255)
    scene_red.add(layer_red, z=0)
    scene_red.do(ac.Delay(2) + ac.CallFunc(pop_scene))
    director.push(SequenceScene(scene_blue, scene_red))


description = '\nUses SequenceScene to push some scenes in the director stack.\nYou should see 2 sec Green, 2 sec Blue, 2 sec Red, forever Green\n'

def main():
    print(description)
    director.init(resizable=True, width=640, height=480)
    scene_green = Scene()
    layer_green = ColorLayer(32, 255, 0, 255)
    scene_green.add(layer_green)
    scene_green.do(ac.Delay(2.0) + ac.CallFunc(push_sequence_scene))
    pyglet.clock.schedule(lambda dt: None)
    director.run(scene_green)


if __name__ == '__main__':
    main()