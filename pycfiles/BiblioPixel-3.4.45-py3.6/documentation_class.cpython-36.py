# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/bibliopixel/animation/documentation_class.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 1686 bytes
from bibliopixel.animation import animation
from bibliopixel.colors import COLORS

class Example26(animation.Animation):

    def __init__(self, *args, color=COLORS.green, **kwds):
        (super().__init__)(*args, **kwds)
        self.color = color

    def step(self, amt=1):
        this_pixel = self.cur_step % len(self.color_list)
        self.color_list[this_pixel - 1] = COLORS.black
        self.color_list[this_pixel] = self.color

    def pre_run(self):
        super().pre_run()

    def cleanup(self, clean_layout=True):
        super().cleanup(clean_layout)


class Example28(Example26):

    def step(self, amt=1):
        this_pixel = self.cur_step % len(self.color_list)
        self.color_list[this_pixel - 1] = COLORS.black
        self.color_list[this_pixel] = self.color
        self.color_list[this_pixel - 2] = COLORS.yellow
        self.color_list[this_pixel - 3] = COLORS.black