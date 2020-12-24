# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/autograd/blocks/trigo.py
# Compiled at: 2018-12-08 17:32:08
# Size of source mod 2**32: 1694 bytes
from autograd.blocks.block import SimpleBlock
import numpy as np

class sin(SimpleBlock):
    __doc__ = '\n    vectorized sinus function on vectors\n    '

    def data_fn(self, args):
        new_data = np.sin(args.data)
        return new_data

    def gradient_fn(self, args):
        grad = np.cos(args.data)
        return grad


class cos(SimpleBlock):
    __doc__ = '\n    vectorized cosine function on vectors\n    '

    def data_fn(self, args):
        new_data = np.cos(args.data)
        return new_data

    def gradient_fn(self, args):
        grad = -np.sin(args.data)
        return grad


class tan(SimpleBlock):
    __doc__ = '\n    vectorized cosine function on vectors\n\t'

    def data_fn(self, args):
        new_data = np.tan(args.data)
        return new_data

    def gradient_fn(self, args):
        grad = 1 / np.cos(args.data) ** 2
        return grad


class arcsin(SimpleBlock):
    __doc__ = '\n    vectorized arcsin function on vectors\n    '

    def data_fn(self, args):
        new_data = np.arcsin(args.data)
        return new_data

    def gradient_fn(self, args):
        grad = 1 / np.sqrt(1 - args.data ** 2)
        return grad


class arccos(SimpleBlock):
    __doc__ = '\n    vectorized arcsin function on vectors\n    '

    def data_fn(self, args):
        new_data = np.arccos(args.data)
        return new_data

    def gradient_fn(self, args):
        grad = -1 / np.sqrt(1 - args.data ** 2)
        return grad


class arctan(SimpleBlock):
    __doc__ = '\n    vectorized arcsin function on vectors\n    '

    def data_fn(self, args):
        new_data = np.arctan(args.data)
        return new_data

    def gradient_fn(self, args):
        grad = 1 / (1 + args.data ** 2)
        return grad