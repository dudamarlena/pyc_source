# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/util/color_list.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 2583 bytes
import copy, numpy
from .limit import Limit

def is_numpy(x):
    return isinstance(x, numpy.ndarray)


def check_numpy(item, name=None):
    if not is_numpy(item.color_list):
        name = name or item.__class__.__name__
        raise ValueError(_NEEDS_NUMPY_ERROR % name)


class ListMath:

    @staticmethod
    def clear(color_list):
        if color_list:
            black = tuple(0 for i in color_list[0])
            color_list[:] = (black for i in color_list)

    @staticmethod
    def add(color_list, source, level=1, buffer=None):

        def add(color, src):
            return tuple(int(c + level * s) for c, s in zip(color, src))

        if level:
            color_list[:] = (add(c, s) for c, s in zip(color_list, source))
        return buffer

    @staticmethod
    def copy(color_list, source):
        color_list[:] = source

    @staticmethod
    def scale(color_list, gain):
        color_list[:] = [tuple(gain * i for i in c) for c in color_list]

    @staticmethod
    def sum(color_list):
        return sum(sum(c) for c in color_list)


class NumpyMath:

    @staticmethod
    def clear(color_list):
        color_list.fill(0)

    @staticmethod
    def add(color_list, source, level=1, buffer=None):
        if level:
            buffer = numpy.multiply(source, level, out=buffer, casting='unsafe')
            color_list += buffer
        return buffer

    @staticmethod
    def copy(color_list, source):
        numpy.copyto(color_list, source, casting='unsafe')

    @staticmethod
    def scale(color_list, gain):
        color_list *= gain

    @staticmethod
    def sum(color_list):
        return sum(sum(c) for c in color_list)


def Math(color_list):
    if is_numpy(color_list):
        return NumpyMath
    else:
        return ListMath


class Mixer:

    def __init__(self, color_list, sources, levels=None):
        self.color_list = color_list
        self.math = Math(color_list)
        self.sources = sources
        self.levels = list(levels or [])
        needed = len(self.sources) - len(self.levels)
        self.levels.extend(0 for i in range(needed))
        self.buffer = None

    def clear(self):
        self.math.clear(self.color_list)

    def mix(self, master=1):
        for source, level in zip(self.sources, self.levels):
            self.buffer = self.math.add(self.color_list, source, level * master, self.buffer)


_NEEDS_NUMPY_ERROR = '%s needs numpy to run.\n\nYou can either:\n\n1. Edit your Project file to add a line\n\n    numbers: float\n\n2. Use the `--numbers` flag`:\n\n    $ bp --numbers=float <your-project-name>.yml\n'