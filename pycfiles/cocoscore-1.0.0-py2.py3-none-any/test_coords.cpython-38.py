# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\test\test_coords.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 2619 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, q'
tags = 'get_virtual_coordinates, mouse hit'
import cocos
import cocos.director as director
from cocos.sprite import Sprite
from cocos.actions import FadeOut, FadeIn
import pyglet
sw = 800
sh = 600

class TestLayer(cocos.layer.ColorLayer):

    def __init__(self):
        super(TestLayer, self).__init__(0, 0, 50, 255)
        sprite = Sprite('fire.png')
        w, h = sprite.width // 2, sprite.height // 2
        self.positions = [
         (
          w, h),
         (
          sw - w, h),
         (
          w, sh - h),
         (
          sw - w, sh - h),
         (
          sw // 2, sh // 2)]
        self.sprites = []
        for pos in self.positions:
            sprite = Sprite('fire.png')
            sprite.position = pos
            self.add(sprite)
            self.sprites.append(sprite)

        self.dd = sprite

    def click(self, x, y):
        for i, (pos_x, pos_y) in enumerate(self.positions):
            ok_x = pos_x - 5 <= x <= pos_x + 5
            ok_y = pos_y - 5 <= y <= pos_y + 5
            if ok_x and ok_y:
                sprite = self.sprites[i]
                sprite.do(FadeOut(0.5) + FadeIn(0.5))
                break


class MouseManager(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self, test):
        super(MouseManager, self).__init__()
        self.test = test

    def on_mouse_press(self, x, y, buttons, modifiers):
        x, y = director.get_virtual_coordinates(x, y)
        self.test.click(x, y)


description = '\nInteractive test checking good behavior of virtual coordinates after resizes.\nClicking the ball center should blink the ball, for any ball, whatever the\nresize done (including fullscreen, done with ctrl + F)\n'

def main():
    print(description)
    director.init(width=sw, height=sh, resizable=True)
    test_layer = TestLayer()
    main_scene = cocos.scene.Scene(test_layer)
    main_scene.add(MouseManager(test_layer))
    director.run(main_scene)


if __name__ == '__main__':
    main()