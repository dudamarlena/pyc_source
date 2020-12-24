# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\test\test_multiple_grid_effects.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 2289 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, t 1, s, t 3, s, t 4, s, t 5, s, t 8.1, s'
tags = 'ShuffleTiles, Flip, ShuffleTiles'
import pyglet
from pyglet.gl import glColor4ub, glPushMatrix, glPopMatrix
import cocos
import cocos.director as director
from cocos.actions import Flip, Waves3D, ShuffleTiles
from cocos.sprite import Sprite
from cocos.layer import Layer, ColorLayer
from cocos.scene import Scene
from pyglet import gl

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


class BackgroundLayer(cocos.layer.Layer):

    def __init__(self):
        super(BackgroundLayer, self).__init__()
        self.img = pyglet.resource.image('background_image.png')

    def draw(self):
        gl.glColor4ub(255, 255, 255, 255)
        gl.glPushMatrix()
        self.transform()
        self.img.blit(0, 0)
        gl.glPopMatrix()


description = '\nAplying different effects to different scene parts. \nThe background does a ShuffleTiles, the layer with sprites does\na Wave3D followed by a Flip.\n'

def main():
    print(description)
    director.init(resizable=True)
    main_scene = Scene()
    back = BackgroundLayer()
    sprite = SpriteLayer()
    main_scene.add(back, z=0)
    main_scene.add(sprite, z=1)
    sprite.do(Waves3D(duration=4) + Flip(duration=4))
    back.do(ShuffleTiles(duration=3, grid=(16, 12)))
    director.run(main_scene)


if __name__ == '__main__':
    main()