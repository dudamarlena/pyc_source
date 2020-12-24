# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/sciann/constraints/data.py
# Compiled at: 2020-03-20 20:49:57
# Size of source mod 2**32: 1350 bytes
""" Data class to impose data constraint.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from .constraint import Constraint
from ..utils import is_functional

class Data(Constraint):
    __doc__ = " Data class to impose to the system.\n\n    # Arguments\n        cond: Functional.\n            The `Functional` object that Data condition\n            will be imposed on.\n        name: String.\n            A `str` for name of the pde.\n\n    # Returns\n\n    # Raises\n        ValueError: 'cond' should be a functional object.\n                    'mesh' should be a list of numpy arrays.\n    "

    def __init__(self, cond, name='data', **kwargs):
        if not is_functional(cond):
            raise ValueError('Expected a Functional object as the `cond`, received a {} - {}'.format(type(cond), cond))
        elif 'x_true_ids' in kwargs or 'y_true' in kwargs:
            raise ValueError('Legacy inputs: please check `SciModel` and `SciModel.train` on how to impose partial data. ')
        else:
            if len(kwargs) > 0:
                raise ValueError('Unrecognized input variable: {}'.format(kwargs.keys()))
        super(Data, self).__init__(cond=cond,
          name=name)