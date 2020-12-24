# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\test\test_rect.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 3911 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, t 3.1, s, t 6.1, s, t 9.1, s, q'
tags = 'get_rect, mouse_hit, collision'
import cocos
import cocos.director as director
from cocos.sprite import Sprite
from cocos.layer import ColorLayer
from cocos.actions import *
import pyglet
from pyglet.gl import *

class TestLayer(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self):
        super(TestLayer, self).__init__()
        self.mouse_x = self.mouse_y = 0
        x, y = director.get_window_size()
        self.sprite1 = Sprite('grossini.png', anchor=(0, 0))
        self.sprite_rect = None
        self.add((self.sprite1), z=2)
        self.sprite1.position = (x // 3, y // 2)
        self.show_rect()
        self.do(Delay(2) + CallFunc(self.mov) + Delay(2) + CallFunc(self.zoom) + Delay(2) + CallFunc(self.scalex) + Delay(2) + CallFunc(self.rot))
        self.mouse_mark = cocos.layer.ColorLayer(0, 0, 255, 255, 20, 20)
        self.add((self.mouse_mark), z=3)

    def show_rect(self):
        if self.sprite_rect:
            self.remove(self.sprite_rect)
        rect = self.sprite1.get_rect()
        self.sprite_rect = ColorLayer(255, 255, 255, 255, width=(rect.width),
          height=(rect.height))
        self.sprite_rect.position = rect.position
        self.add((self.sprite_rect), z=1)

    def mov(self):
        x, y = director.get_window_size()
        self.sprite1.position = (x * 2 // 3, y // 2)
        self.show_rect()

    def rot(self):
        self.sprite1.rotation = 90
        self.show_rect()

    def zoom(self):
        self.sprite1.scale = 2
        self.show_rect()

    def scalex(self):
        self.sprite1.scale_x = 0.5
        self.show_rect()

    def on_mouse_press(self, x, y, buttons, modifiers):
        self.update_mouse_mark(x, y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.update_mouse_mark(x, y)

    def update_mouse_mark(self, x, y):
        x, y = director.get_virtual_coordinates(x, y)
        self.mouse_mark.position = (x - 5, y - 5)
        rect = self.sprite1.get_rect()
        if rect.contains(x, y):
            self.mouse_mark.color = (255, 0, 0)
        else:
            self.mouse_mark.color = (0, 0, 255)


description = '\nIn very simple cases Sprite.get_rect can be used to check for collisions\nbetween sprites or between a sprite and the mouse position.\n\nTo work as expected these conditions must be meet:\n    Both sprites are direct childs of the same node\n    The sprite(s) image anchor must be (0,0)\n    sprite.rotation == 0 for both sprites.\n\nThis scripts shows a sprite and a white rectangle depicting sprite.get_rect(),\n    It starts at one position\n    After 2 seconds sprite moves to another position\n    After 2 seconds sprite scales 2x in both axis\n    After 2 seconds sprite scales 0.5 in the x axis\n    After 2 seconds sprite rotates 90 degress\n\nget_rect() gives a tight fit when changing position or scale, but not when a\nrotation is applied.\nClicking or draging into the get_rect() changes the colored square that follows\nthe mouse to red; when outside the get_rect() it turns blue. \n\nFor other variants on collision or mouse hit see\n    test/test_sprite_aabb.py,\n    samples/balldrive_toy_game\n    samples/mouse_elastic_box_selection.py\n'

def main():
    print(description)
    director.init()
    test_layer = TestLayer()
    main_scene = cocos.scene.Scene(test_layer)
    director.run(main_scene)


if __name__ == '__main__':
    main()