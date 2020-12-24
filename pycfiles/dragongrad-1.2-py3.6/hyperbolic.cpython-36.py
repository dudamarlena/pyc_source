# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/autograd/blocks/hyperbolic.py
# Compiled at: 2018-11-15 12:27:13
# Size of source mod 2**32: 867 bytes
from autograd.blocks.block import SimpleBlock
import numpy as np

class sinh(SimpleBlock):
    __doc__ = '\n    vectorized sin h function on vectors\n    '

    def data_fn(self, args):
        new_data = np.sinh(args.data)
        return new_data

    def gradient_fn(self, args):
        grad = np.cosh(args.data)
        return grad


class cosh(SimpleBlock):
    __doc__ = '\n    vectorized cosine h function on vectors\n    '

    def data_fn(self, args):
        new_data = np.cosh(args.data)
        return new_data

    def gradient_fn(self, args):
        grad = np.sinh(args.data)
        return grad


class tanh(SimpleBlock):
    __doc__ = '\n    vectorized tan h function on vectors\n    '

    def data_fn(self, args):
        new_data = np.tanh(args.data)
        return new_data

    def gradient_fn(self, args):
        grad = 1 - np.tanh(args.data) ** 2
        return grad