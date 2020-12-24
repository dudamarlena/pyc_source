# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/swails/src/ParmEd/parmed/symmetry.py
# Compiled at: 2017-03-01 21:14:20
# Size of source mod 2**32: 370 bytes
import numpy as np

class Symmetry(object):
    __doc__ = 'Symmetry operations\n\n    Parameters\n    ----------\n    tensor : np.array, shape=(3*n_symmetry, 4)\n    '

    def __init__(self, tensor):
        self.data = np.asarray(tensor, dtype='f8')
        if self.data.ndim != 2 or self.data.shape[1] != 4:
            raise ValueError('Tensor shape must be (3*n_symmetry, 4)')