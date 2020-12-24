# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/daniel/Programming/python/joy2mouse/joy2mouselib/mouse.py
# Compiled at: 2011-06-07 03:10:47
from Xlib.display import Display
from Xlib import X
from Xlib.ext.xtest import fake_input

class Mouse:

    def __init__(self):
        self.display = Display()

    def press(self, button=1):
        print button, 'press'
        fake_input(self.display, X.ButtonPress, [None, 1, 3, 2, 4, 5][button])
        self.display.sync()
        return

    def release(self, button=1):
        print button, 'release'
        fake_input(self.display, X.ButtonRelease, [None, 1, 3, 2, 4, 5][button])
        self.display.sync()
        return

    def click(self, button=1):
        print button, 'click'
        self.press(button)
        self.release(button)

    def move(self, x, y):
        fake_input(self.display, X.MotionNotify, x=x, y=y)

    def position(self):
        coord = self.display.screen().root.query_pointer()._data
        return (coord['root_x'], coord['root_y'])

    def move_relative(self, x=0, y=0):
        cur_x, cur_y = self.position()
        self.move(cur_x + x, cur_y + y)

    def screen_size(self):
        width = self.display.screen().width_in_pixels
        height = self.display.screen().height_in_pixels
        return (width, height)


if __name__ == '__main__':
    m = Mouse()
    m.move_relative(100)
    m.move_relative(100)