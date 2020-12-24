# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/util/keyword_args.py
# Compiled at: 2018-06-15 01:22:48
# Size of source mod 2**32: 1657 bytes
"""Keyword args functions."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import functools
from tensorflow.python.util import decorator_utils

def keyword_args_only(func):
    """Decorator for marking specific function accepting keyword args only.

  This decorator raises a `ValueError` if the input `func` is called with any
  non-keyword args. This prevents the caller from providing the arguments in
  wrong order.

  Args:
    func: The function or method needed to be decorated.

  Returns:
    Decorated function or method.

  Raises:
    ValueError: If `func` is not callable.
  """
    decorator_utils.validate_callable(func, 'keyword_args_only')

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        """Keyword args only wrapper."""
        if args:
            raise ValueError('Must use keyword args to call {}.'.format(func.__name__))
        return func(**kwargs)

    return new_func