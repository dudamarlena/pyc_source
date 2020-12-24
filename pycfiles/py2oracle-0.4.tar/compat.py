# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/py2opencl/compat.py
# Compiled at: 2014-11-11 10:50:58
import numpy as np

class SafeArray(np.ndarray):

    @staticmethod
    def wrap(arr):
        return arr.view(SafeArray)

    def __getitem__(self, index):
        if type(index) is int:
            index = index % self.shape[0]
        elif type(index) is tuple:
            t = []
            for x, size in zip(index, self.shape):
                if type(x) is int:
                    t.append(x % size)
                else:
                    t.append(x)

            index = tuple(t)
        return super(SafeArray, self).__getitem__(index)