# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\cocos2020\test\test_grid_effect_in_layer.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 1610 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, t 1, s, t 2.1, s, t 3.2, s, t 4.1, s, q'
tags = 'Layer, Waves3D, Flip'
import cocos.director as director
from cocos.actions import Flip, Waves3D
from cocos.sprite import Sprite
from cocos.layer import Layer, ColorLayer
from cocos.scene import Scene

class SpriteLayer(Layer):

    def __init__(self):
        super(SpriteLayer, self).__init__()
        sprite1 = Sprite('grossini.png')
        sprite2 = Sprite('grossinis_sister1.png')
        sprite3 = Sprite('grossinis_sister2.png')
        sprite1.position = (400, 240)
        sprite2.position = (300, 240)
        sprite3.position = (500, 240)
        self.add(sprite1)
        self.add(sprite2)
        self.add(sprite3)


description = '\nA scaled-down ColorLayer and three sprites, the scene at fist waves and\nthen flips trough the use of Waves3D and Flip actions over the holder Layer \n'

def main():
    print(description)
    director.init(resizable=True)
    main_scene = Scene()
    red = ColorLayer(255, 0, 0, 128)
    sprite = SpriteLayer()
    red.scale = 0.75
    main_scene.add(red, z=0)
    main_scene.add(sprite, z=1)
    sprite.do(Waves3D(duration=2) + Flip(duration=2))
    director.run(main_scene)


if __name__ == '__main__':
    main()