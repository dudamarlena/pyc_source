# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/getml/loss_functions.py
# Compiled at: 2019-10-22 02:44:50
# Size of source mod 2**32: 2210 bytes
"""
This module contains the loss functions for the getml library.
"""

class _LossFunction(object):
    __doc__ = '\n    Base class. Should not ever be directly initialized!\n    '

    def __init__(self):
        self.thisptr = dict()
        self.thisptr['type_'] = 'none'


class CrossEntropyLoss(_LossFunction):
    __doc__ = '\n    Cross entropy function.\n\n    Recommended loss function for classification problems.\n    '

    def __init__(self):
        super(CrossEntropyLoss, self).__init__()
        self.thisptr['type_'] = 'CrossEntropyLoss'


class SquareLoss(_LossFunction):
    __doc__ = '\n    Square loss function.\n\n    Recommended loss function for regression problems.\n    '

    def __init__(self):
        super(SquareLoss, self).__init__()
        self.thisptr['type_'] = 'SquareLoss'