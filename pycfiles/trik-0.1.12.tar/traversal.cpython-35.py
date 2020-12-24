# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\trik\trik\yu\traversal.py
# Compiled at: 2020-04-12 22:57:27
# Size of source mod 2**32: 940 bytes
import numpy

def array_index_traversal(array_shape):
    scale = numpy.prod(array_shape)
    for i in range(scale):
        index = [
         0] * len(array_shape)
        index[-1] = i
        for r in range(len(array_shape) - 1, -1, -1):
            if index[r] >= array_shape[r]:
                index[r - 1] = index[r] // array_shape[r]
                index[r] %= array_shape[r]
            else:
                break

        yield tuple(index)


def multi_range(range_list):
    len_list = [len(r) for r in range_list]
    scale = numpy.prod(len_list)
    for i in range(scale):
        index = [
         0] * len(len_list)
        index[-1] = i
        for r in range(len(len_list) - 1, -1, -1):
            if index[r] >= len_list[r]:
                index[r - 1] = index[r] // len_list[r]
                index[r] %= len_list[r]
            else:
                break

        yield tuple(range_list[_i][_index] for _i, _index in enumerate(index))