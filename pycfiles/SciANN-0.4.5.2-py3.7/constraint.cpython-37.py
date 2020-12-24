# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/sciann/constraints/constraint.py
# Compiled at: 2020-03-20 20:49:57
# Size of source mod 2**32: 1642 bytes
""" Constraint class to condition on the training.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from ..utils import is_tensor

class Constraint(object):
    __doc__ = ' Configures the condition to impose constraint.\n\n    # Arguments\n        var: The layer name to impose the constraint.\n        cond: A callable handle to function that imposes the condition.\n        name: A `str` to be associated to the constraint.\n\n    # Returns\n\n    # Raises\n        ValueError if `model` is not of class `SciModel`.\n        ValueError for unrecognized inputs.\n    '

    def __init__(self, var=None, cond=None, name=None, **kwargs):
        if not isinstance(var, (str, type(None))):
            raise AssertionError('Expected a Layer Name of type str. ')
        else:
            if not cond is None:
                if not callable(cond):
                    assert is_tensor(cond), 'Expected a function or a Tensor as input. '
            if 'ids' in kwargs or 'sol' in kwargs:
                raise ValueError('Legacy interface: please use `SciModel` and `SciModel.train` to impose on specific ids. ')
            else:
                if len(kwargs) > 0:
                    raise ValueError('Unrecognized input variable: {}'.format(kwargs.keys()))
        assert isinstance(name, (str, type(None))), 'Expected a string input for the name. '
        self.var = var
        self.cond = cond
        self.name = name

    def __call__(self):
        return self.cond

    def eval(self, xs):
        return self.cond.eval(xs)