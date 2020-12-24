# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\cocos2020\test\test_accel_amplitude.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 1644 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 1, s, t 7, s, t 8, s, t 10.1, s, q'
tags = 'grid_actions, AccelAmplitude, Waves3D'
import pyglet, cocos
import cocos.director as director
from cocos.actions import *
from cocos.layer import *
from pyglet import gl

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


description = '\nShows how to use AccelAmplitude to modify a GridAction.\nAccelAction will reparametrize time for the target action.\nIt should be seen the stock background shaken with waves of increasing\nmagnitude, begginning with a flat image.\n'

def main():
    print(description)
    director.init(resizable=True)
    main_scene = cocos.scene.Scene()
    main_scene.add((BackgroundLayer()), z=0)
    action1 = Waves3D(waves=16, amplitude=80, grid=(16, 16), duration=10)
    action2 = AccelAmplitude(action1, rate=4.0)
    main_scene.do(action2)
    director.run(main_scene)


if __name__ == '__main__':
    main()