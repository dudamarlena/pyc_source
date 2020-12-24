# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/sciann/constraints/pde.py
# Compiled at: 2020-03-20 20:49:57
# Size of source mod 2**32: 1260 bytes
""" PDE class to impose pde constraint.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from .constraint import Constraint
from ..utils import is_functional

class PDE(Constraint):
    __doc__ = " PDE class to impose to the system.\n\n    # Arguments\n        pde: Functional.\n            The `Functional` object that pde if formed on.\n        name: String.\n            A `str` for name of the pde.\n\n    # Returns\n\n    # Raises\n        ValueError: 'pde' should be a functional object.\n    "

    def __init__(self, pde, name='pde', **kwargs):
        if not is_functional(pde):
            raise ValueError('Expected a Functional object as the pde, received a {} - {}'.format(type(pde), pde))
        elif 'mesh_ids' in kwargs or 'sol' in kwargs:
            raise ValueError('Legacy interface: please use `SciModel` and `SciModel.train` to impose on specific ids. ')
        else:
            if len(kwargs) > 0:
                raise ValueError('Unrecognized input variable: {}'.format(kwargs.keys()))
        super(PDE, self).__init__(cond=pde,
          name=name)