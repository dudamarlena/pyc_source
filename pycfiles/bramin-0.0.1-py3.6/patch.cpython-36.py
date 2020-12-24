# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bramin/patch.py
# Compiled at: 2019-10-28 23:29:52
# Size of source mod 2**32: 634 bytes
import typing as t
from functools import wraps, partial

def patch_op(obj, op):
    from .pipe import Pipe
    real = getattr(obj, op)

    @wraps(real)
    def fake(self, other):
        if other is Pipe:
            return NotImplemented
        else:
            return real(self, other)

    setattr(obj, op, fake)
    return obj


def patch_all():
    """substitute __or__ method, for use 'obj | P | func' synatax"""
    patch = partial(patch_op, op='__or__')
    try:
        import pandas as pd
        patch(pd.DataFrame)
        patch(pd.Series)
        patch(pd.Index)
    except ImportError:
        pass