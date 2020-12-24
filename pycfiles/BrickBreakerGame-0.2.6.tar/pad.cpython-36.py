# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/uros/Projects/BrickBreaker/BrickBreaker/pad.py
# Compiled at: 2017-12-13 09:34:09
# Size of source mod 2**32: 1133 bytes
from BrickBreaker.Shared import *

class Pad(GameObject):

    def __init__(self, position, image):
        self.left_is_pressed = False
        self.right_is_pressed = False
        self._mouse = False
        self._keyboard = True
        super().__init__(position, GameConstants.PAD_SIZE, image)

    def set_position(self, position):
        new_position = [
         position[0], position[1]]
        size = self.get_size()
        if new_position[0] + size[0] > GameConstants.SCREEN_SIZE[0]:
            new_position[0] = GameConstants.SCREEN_SIZE[0] - size[0]
        if new_position[0] < 0:
            new_position[0] = 0
        super().set_position(new_position)

    def left_pressed(self, pressed):
        self.left_is_pressed = pressed

    def right_pressed(self, pressed):
        self.right_is_pressed = pressed

    def activate_mouse(self):
        self._mouse = True
        self._keyboard = False

    def activate_keyboard(self):
        self._mouse = False
        self._keyboard = True

    def get_mouse_status(self):
        return self._mouse

    def get_keyboard_status(self):
        return self._keyboard