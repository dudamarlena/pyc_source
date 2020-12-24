# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/sciann/constraints/minmax.py
# Compiled at: 2020-03-20 20:49:57
# Size of source mod 2**32: 1721 bytes
""" PDE class to impose pde constraint.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from .constraint import Constraint
from ..utils import is_functional
from ..utils import relu, sign, abs, tanh

class MinMax(Constraint):
    __doc__ = "MinMax weight constraint.\n\n    Constrains the weights incident to each hidden unit\n    to have values between a lower bound and an upper bound.\n\n    # Arguments\n        min_value: the minimum norm for the incoming weights.\n        max_value: the maximum norm for the incoming weights.\n\n    # Raises\n        ValueError: 'cond' should be a functional object.\n    "

    def __init__(self, cond, min_value=None, max_value=None, penalty=1.0, name='minmax'):
        if not is_functional(cond):
            raise ValueError('Expected a Functional object, received a {} - {}'.format(type(cond), cond))
        else:
            if min_value is not None:
                if max_value is not None:
                    if min_value > max_value:
                        raise ValueError('Check inputs: `min_value` should be smaller than `max_value`. ')
            try:
                delta = max_value - min_value
                const = 0.0
                if min_value is not None:
                    const += (1.0 - sign(cond - min_value)) * abs(cond - min_value)
                if max_value is not None:
                    const += (1.0 + sign(cond - max_value)) * abs(cond - max_value)
                const *= penalty
            except (ValueError, TypeError):
                assert False, 'Unexpected error - cannot evaluate the regularization. '

        super(MinMax, self).__init__(cond=const,
          name=name)