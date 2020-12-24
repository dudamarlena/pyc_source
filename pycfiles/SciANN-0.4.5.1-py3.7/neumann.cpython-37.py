# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/sciann/constraints/neumann.py
# Compiled at: 2020-03-20 20:49:57
# Size of source mod 2**32: 2663 bytes
""" Neumann class to impose data Neumann constraint.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from .constraint import *

class Neumann(Constraint):
    __doc__ = " Dirichlet class to impose to the system.\n\n    # Arguments\n        cond: Functional.\n            The `Functional` object that Neumann condition\n            will be imposed on.\n        sol: np.ndarray.\n            Expected output to set the `pde` to.\n            If not provided, will be set to `zero`.\n        mesh_ids: np.ndarray.\n            A 1D numpy arrays consists of node-ids to impose the condition.\n        var: String.\n            A layer name to differentiate `cond` with respect to.\n        name: String.\n            A `str` for name of the pde.\n\n    # Returns\n\n    # Raises\n        ValueError: 'cond' should be a functional object.\n                    'mesh' should be a list of numpy arrays.\n    "

    def __init__(self, cond, sol=None, mesh_ids=None, var=None, name='neumann'):
        if not is_functional(cond):
            raise ValueError('Expected a Functional object as the `cond`, received a {} - {}'.format(type(cond), cond))
        else:
            if isinstance(var, str):
                cond = cond.diff(var)
            else:
                raise NotImplementedError('Currently, only differentiation with respect to layers are supported. ')
            if mesh_ids is not None:
                if not all([isinstance(mesh_ids, np.ndarray), mesh_ids.ndim == 1]):
                    raise ValueError('Expected a 1d numpy arrays of mesh ids, received a {} - {}'.format(type(mesh_ids), mesh_ids))
            if sol is not None:
                sol = to_list(sol)
                if not all([isinstance(x, np.ndarray) for x in sol]):
                    raise ValueError('Expected a list of numpy arrays for `sol`, received a {} - {}'.format(type(sol), sol))
                if len(sol) != len(cond.outputs):
                    raise ValueError('Number of expected outputs in `sol` does not match number of outputs from the constraint. \n Provided {} \nExpected {} '.format(sol, cond.outputs))
        super(Neumann, self).__init__(cond=cond,
          ids=mesh_ids,
          sol=sol,
          name=name)