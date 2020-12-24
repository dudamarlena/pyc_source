# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/util/tf_contextlib.py
# Compiled at: 2018-06-15 01:22:48
# Size of source mod 2**32: 1377 bytes
"""TFDecorator-aware replacements for the contextlib module."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import contextlib as _contextlib
from tensorflow.python.util import tf_decorator

def contextmanager(target):
    """A tf_decorator-aware wrapper for `contextlib.contextmanager`.

  Usage is identical to `contextlib.contextmanager`.

  Args:
    target: A callable to be wrapped in a contextmanager.
  Returns:
    A callable that can be used inside of a `with` statement.
  """
    context_manager = _contextlib.contextmanager(target)
    return tf_decorator.make_decorator(target, context_manager, 'contextmanager')