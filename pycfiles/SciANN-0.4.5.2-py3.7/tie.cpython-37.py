# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/sciann/constraints/tie.py
# Compiled at: 2020-03-20 20:49:57
# Size of source mod 2**32: 2029 bytes
""" Tie constraint to tie different outputs of the network.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from .constraint import Constraint
from ..utils import is_functional

class Tie(Constraint):
    __doc__ = " Tie class to constrain network outputs.\n        constraint: `cond1 - cond2 == sol`.\n\n    # Arguments\n        cond1: Functional.\n            A `Functional` object to be tied to cond2.\n        cond2: Functional.\n            A 'Functional' object to be tied to cond1.\n        name: String.\n            A `str` for name of the pde.\n\n    # Returns\n\n    # Raises\n        ValueError: 'pde' should be a functional object.\n    "

    def __init__(self, cond1, cond2, name='tie', **kwargs):
        if not is_functional(cond1):
            raise ValueError('Expected a Functional object as the cond1, received a {} - {}'.format(type(cond1), cond1))
        else:
            if not is_functional(cond2):
                raise ValueError('Expected a Functional object as the cond2, received a {} - {}'.format(type(cond2), cond2))
            try:
                cond = cond1 - cond2
            except (ValueError, TypeError):
                print('Unexpected ValueError/TypeError - ', 'make sure `cond1` and `cond2` are functional objects. \n', 'cond1 - {} \n'.format(cond1), 'cond2 - {} \n'.format(cond2))

            if 'mesh_ids' in kwargs or 'sol' in kwargs:
                raise ValueError('Legacy interface: please use `SciModel` and `SciModel.train` to impose on specific ids. ')
            else:
                if len(kwargs) > 0:
                    raise ValueError('Unrecognized input variable: {}'.format(kwargs.keys()))
        super(Tie, self).__init__(cond=cond,
          name=name)