# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/animation/sequence.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 1557 bytes
from . import wrapper
from ..util import log
import random as rand

class Sequence(wrapper.Indexed):

    def __init__(self, layout, random=False, length=None, **kwds):
        """
        Arguments

        random -- If True, a random animation is selected each step
        length -- if length is a number, run all the animations in a loop
            for `length` seconds each.  If `length` is a list of numbers,
            use the numbers successively as times.
        """
        (super().__init__)(layout, **kwds)
        self.random = random
        if isinstance(length, (list, tuple)):
            self.length = length
        else:
            self.length = length and [length]

    def restart(self):
        self.random and rand.shuffle(self.animations)
        self.index = 0

    def pre_run(self):
        self.offset = 0
        super().pre_run()
        self.restart()

    def step(self, amt=1):
        if not self.animations or super().step(amt):
            return
        self.index += 1
        if self.index >= len(self.animations):
            if self.runner.until_complete:
                self.completed = True
            else:
                self.offset += len(self.animations)
                self.restart()

    def _on_index(self, old_index):
        if self.current_animation:
            super()._on_index(old_index)
            if self.length:
                step = self.offset + self.index
                length = self.length[(step % len(self.length))]
                self.current_animation.runner.seconds = length