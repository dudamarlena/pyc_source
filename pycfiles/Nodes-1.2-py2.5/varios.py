# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/nodes/varios.py
# Compiled at: 2009-06-08 07:12:47
"""Randomization functions."""
from core import Synaps
import random

class VariositiedSynaps(Synaps):

    def __init__(self, variosity):
        assert variosity <= 1
        self.variosity = variosity

    def __getattribute__(self, attr):
        if self.__dict__.has_key(attr):
            if self.dict.has_key('null_' + attr):
                if random.random() > self.variosity:
                    attr = 'null_' + attr
            return super(Synaps, self).__getattribute__(attr)
        else:
            raise AttributeError

    def null_get(self):
        return

    def null_back_propagate(self, value):
        pass

    def null_put(self, value):
        self.retry = value


class NullSynaps(Synaps):

    def __init__(self):
        pass

    def get(self):
        return

    def put(self, value):
        pass

    def back_propagate(self, value):
        pass


def RandomSynaps(variosity):
    class_ = Synaps
    if random.random() > variosity:
        class_ = NullSynaps
    return class_()