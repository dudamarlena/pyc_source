# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/juancomish/miniconda3/lib/python3.7/site-packages/pyehub/energy_hub/utils.py
# Compiled at: 2019-07-03 19:21:52
# Size of source mod 2**32: 1556 bytes
__doc__ = '\nProvides some utility functions for all code in energy_hub.\n'
import functools

def cached_property(func):
    """Return a property that caches results.

    Args:
        func: The function to decorated

    Returns:
        The decorated cached property
    """

    @property
    @functools.lru_cache(maxsize=1)
    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return _wrapper


def constraint(*args, enabled=True):
    """
    Mark a function as a constraint of the model.

    The function that adds these constraints to the model is
    `_add_indexed_constraints`.

    Args:
        *args: The indices that the constraint is indexed by. Each element of
            each index is passed to the method.
        enabled: Is the constraint enabled? Defaults to True.

    Returns:
        The decorated function
    """

    def _wrapper(func):
        functools.wraps(func)
        func.is_constraint = True
        func.args = args
        func.enabled = enabled
        return func

    return _wrapper


def constraint_list(*, enabled=True):
    """
    Mark a function as a ConstraintList of the model.

    The function has to return a generator. ie: must use a yield in the method
    body.

    Args:
        enabled: Is the constraint enabled? Defaults to True.

    Returns:
        The decorated function
    """

    def _wrapper(func):
        functools.wraps(func)
        func.is_constraint_list = True
        func.enabled = enabled
        return func

    return _wrapper