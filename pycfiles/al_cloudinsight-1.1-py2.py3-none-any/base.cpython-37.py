# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\python\envs\alyvix\alyvix_py37\lib\site-packages\alyvix\core\interaction\mouse\base.py
# Compiled at: 2019-11-11 12:27:44
# Size of source mod 2**32: 1602 bytes
from alyvix.tools.screen import ScreenManager

class MouseManagerBase(object):

    def __init__(self):
        self.left_button = 1
        self.right_button = 2
        self.middle_button = 3
        self.wheel_up = 4
        self.wheel_down = 5
        self.wheel_left = 6
        self.wheel_right = 7
        sm = ScreenManager()
        self._scaling_factor = sm.get_scaling_factor()

    def click(self, x, y, button=1, n=1):
        raise NotImplementedError

    def move(self, x, y):
        raise NotImplementedError

    def scroll(self, step, direction):
        raise NotImplementedError

    def drag(self, x1, y1, x2, y2, button=1):
        raise NotImplementedError