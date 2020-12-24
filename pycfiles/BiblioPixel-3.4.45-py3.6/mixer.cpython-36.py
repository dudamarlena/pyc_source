# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/animation/mixer.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 648 bytes
import copy
from . import parallel
from ..util import color_list

class Mixer(parallel.Parallel):

    def __init__(self, *args, levels=None, master=1, **kwds):
        self.master = master
        (super().__init__)(*args, **kwds)
        self.mixer = color_list.Mixer(self.color_list, [a.color_list for a in self.animations], levels)

    @property
    def levels(self):
        return self.mixer.levels

    @levels.setter
    def levels(self, levels):
        self.mixer.levels[:] = levels

    def step(self, amt=1):
        super().step(amt)
        self.mixer.clear()
        self.mixer.mix(self.master)