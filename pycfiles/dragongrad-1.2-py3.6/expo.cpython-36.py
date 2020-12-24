# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/autograd/blocks/expo.py
# Compiled at: 2018-12-12 06:22:23
# Size of source mod 2**32: 1646 bytes
from autograd.blocks.block import SimpleBlock
import numpy as np

class exp(SimpleBlock):
    __doc__ = '\n    exponential function on vectors\n    '

    def data_fn(self, args):
        new_data = np.exp(args.data)
        return new_data

    def gradient_fn(self, args):
        grad = np.exp(args.data)
        return grad


class log(SimpleBlock):
    __doc__ = '\n    log function on vectors\n    '

    def __init__(self, base=np.e):
        super().__init__()
        self.base = base

    def data_fn(self, args):
        if self.base == np.e:
            new_data = np.log(args.data)
        else:
            if self.base == 10:
                new_data = np.log10(args.data)
            else:
                if self.base == 2:
                    new_data = np.log2(args.data)
                else:
                    if self.base < 0 or self.base == 0:
                        raise ValueError('wrong base, negative or base=1')
                    else:
                        new_data = np.log(args.data) / np.log(self.base)
        return new_data

    def gradient_fn(self, args):
        grad = 1 / (args.data * np.log(self.base))
        return grad


class sqrt(SimpleBlock):
    __doc__ = '\n    square root function on vectors\n    '

    def data_fn(self, args):
        new_data = np.sqrt(args.data)
        return new_data

    def gradient_fn(self, args):
        grad = 1 / (2 * np.sqrt(args.data))
        return grad


class logistic(SimpleBlock):
    __doc__ = '\n    exponential function on vectors\n    '

    def data_fn(self, args):
        new_data = 1 / (1 + np.exp(-args.data))
        return new_data

    def gradient_fn(self, args):
        expo = np.exp(args.data)
        grad = expo / (1 + expo) ** 2
        return grad