# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/animation/split.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 1623 bytes
"""
Split is an animation.Collection that runs multiple smaller animations as
segments within a larger diplay.

"""
import copy
from .parallel import Parallel
from ..layout.strip import Strip

class Split(Parallel):

    def __init__(self, *args, size=100, **kwds):
        """
        Arguments --
            size: a number or a list of numbers representing the size of each
                segment from the original layout.  If there aren't enough sizes
                for each segment, the list of sizes is reused repeatedly.
        """
        (super().__init__)(args, detach=False, **kwds)
        if not size:
            raise ValueError('Split must have at least one size')
        self.size = size if isinstance(size, list) else [size]
        self.is_numpy = hasattr(self.color_list, 'dtype')
        for animation, begin, end in self._foreach():
            animation.layout = Strip([], color_list=(self.color_list[begin:end]))

    def step(self, amt=1):
        super().step(amt)
        if not self.is_numpy:
            for animation, begin, end in self._foreach():
                self.color_list[begin:end] = animation.color_list

    def _foreach(self):
        begin = 0
        for i, animation in enumerate(self.animations):
            end = begin + self.size[(i % len(self.size))]
            if animation:
                yield (
                 animation, begin, end)
            begin = end