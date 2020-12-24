# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\cocos2020\test\test_custom_on_resize.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 3621 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, t 2.1, s, q'
tags = 'director.on_cocos_resize'
autotest = 0
import pyglet
from pyglet.gl import *
import cocos
import cocos.director as director
from cocos.sprite import Sprite
from cocos.actions import Delay, CallFunc
description = '\nThis script demonstrates:\n    How to listen to director events, in particular the on_cocos_resize event.\n    Instruct the director to not autoscale the scene when the window is\n    resized.\n\nWhat you should see:\n    The window shows the usual background pic and three grossinis, resizing\n    the window should show more o less from the scene, at the same scale, and\n    the scene center will always match the window center.\n'

def resize():
    director.window.set_size(800, 600)


class AutocenteredBackgroundLayer(cocos.layer.Layer):
    __doc__ = '\n    An unusual CocosNode that auto centers in the window when a resize happens.\n    For doing that, it registers to the event on_cocos_resize and repositions\n    itself whenever the event happens.\n    '

    def __init__(self):
        super(AutocenteredBackgroundLayer, self).__init__()
        self.img = pyglet.resource.image('background_image.png')
        self.transform_anchor = (0, 0)

    def on_enter(self):
        super(AutocenteredBackgroundLayer, self).on_enter()
        director.push_handlers(self.on_cocos_resize)
        if autotest:
            self.do(Delay(2.0) + CallFunc(resize))

    def on_exit(self):
        director.remove_handlers(self.on_cocos_resize)
        super(AutocenteredBackgroundLayer, self).on_exit()
        self.on_cocos_resize(director._usable_width, director._usable_height)

    def draw(self):
        glColor4ub(255, 255, 255, 255)
        glPushMatrix()
        self.transform()
        self.img.blit(0, 0)
        glPopMatrix()

    def on_cocos_resize(self, usable_width, usable_height):
        x = (usable_width - self.img.width * self.scale) // 2
        y = (usable_height - self.img.height * self.scale) // 2
        self.position = (x, y)


def main():
    print(description)
    director.init(width=400, height=400, autoscale=False, resizable=True)
    scene = cocos.scene.Scene()
    bg = AutocenteredBackgroundLayer()
    for i in range(3):
        sp = Sprite('grossini.png', position=(140 + i * 180, 120))
        bg.add(sp)
    else:
        scene.add(bg)
        director.run(scene)


if __name__ == '__main__':
    main()