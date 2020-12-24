# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\cocos2020\test\test_text_movement.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 2137 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, t 1.1, s, t 2.1, s, q'
tags = 'on_mouse_motion, Label'
autotest = 0
import cocos
from cocos.actions import Delay, CallFunc
import cocos.director as director

class HelloWorld(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self):
        super(HelloWorld, self).__init__()
        self.label = cocos.text.Label('Hi', font_name='Times New Roman',
          font_size=32,
          x=320,
          y=240,
          anchor_x='center',
          anchor_y='center')
        self.add(self.label)
        if autotest:
            self.do(Delay(1) + CallFunc(self.move_label, 100, 100) + Delay(1) + CallFunc(self.move_label, 500, 300))

    def on_mouse_motion(self, x, y, dx, dy):
        if not autotest:
            vh, vy = director.get_virtual_coordinates(x, y)
            self.move_label(vh, vy)

    def move_label(self, x, y):
        self.label.element.text = '%d,%d' % (x, y)
        self.label.element.x = x
        self.label.element.y = y


description = "\nA label its shown, initially 'Hi' at screen center, then telling the\nmouse position at position near the mouse pointer\n"

def main():
    print(description)
    director.init()
    hello_layer = HelloWorld()
    main_scene = cocos.scene.Scene(hello_layer)
    director.run(main_scene)


if __name__ == '__main__':
    main()