# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/util/tf_inspect.py
# Compiled at: 2018-06-15 01:22:48
# Size of source mod 2**32: 4988 bytes
"""TFDecorator-aware replacements for the inspect module."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import inspect as _inspect
from tensorflow.python.util import tf_decorator
ArgSpec = _inspect.ArgSpec

def currentframe():
    """TFDecorator-aware replacement for inspect.currentframe."""
    return _inspect.stack()[1][0]


def getargspec(object):
    """TFDecorator-aware replacement for inspect.getargspec.

  Args:
    object: A callable, possibly decorated.

  Returns:
    The `ArgSpec` that describes the signature of the outermost decorator that
    changes the callable's signature. If the callable is not decorated,
    `inspect.getargspec()` will be called directly on the callable.
  """
    decorators, target = tf_decorator.unwrap(object)
    return next((d.decorator_argspec for d in decorators if d.decorator_argspec is not None), _inspect.getargspec(target))


def getcallargs(func, *positional, **named):
    """TFDecorator-aware replacement for inspect.getcallargs.

  Args:
    func: A callable, possibly decorated
    *positional: The positional arguments that would be passed to `func`.
    **named: The named argument dictionary that would be passed to `func`.

  Returns:
    A dictionary mapping `func`'s named arguments to the values they would
    receive if `func(*positional, **named)` were called.

  `getcallargs` will use the argspec from the outermost decorator that provides
  it. If no attached decorators modify argspec, the final unwrapped target's
  argspec will be used.
  """
    argspec = getargspec(func)
    call_args = named.copy()
    this = getattr(func, 'im_self', None) or getattr(func, '__self__', None)
    if ismethod(func):
        if this:
            positional = (
             this,) + positional
    remaining_positionals = [arg for arg in argspec.args if arg not in call_args]
    call_args.update(dict(zip(remaining_positionals, positional)))
    default_count = 0 if not argspec.defaults else len(argspec.defaults)
    if default_count:
        for arg, value in zip(argspec.args[-default_count:], argspec.defaults):
            if arg not in call_args:
                call_args[arg] = value
                continue

    return call_args


def getdoc(object):
    """TFDecorator-aware replacement for inspect.getdoc.

  Args:
    object: An object, possibly decorated.

  Returns:
    The docstring associated with the object.

  The outermost-decorated object is intended to have the most complete
  documentation, so the decorated parameter is not unwrapped.
  """
    return _inspect.getdoc(object)


def getfile(object):
    """TFDecorator-aware replacement for inspect.getfile."""
    return _inspect.getfile(tf_decorator.unwrap(object)[1])


def getmembers(object, predicate=None):
    """TFDecorator-aware replacement for inspect.getmembers."""
    return _inspect.getmembers(object, predicate)


def getmro(cls):
    """TFDecorator-aware replacement for inspect.getmro."""
    return _inspect.getmro(cls)


def getsource(object):
    """TFDecorator-aware replacement for inspect.getsource."""
    return _inspect.getsource(tf_decorator.unwrap(object)[1])


def isclass(object):
    """TFDecorator-aware replacement for inspect.isclass."""
    return _inspect.isclass(tf_decorator.unwrap(object)[1])


def isfunction(object):
    """TFDecorator-aware replacement for inspect.isfunction."""
    return _inspect.isfunction(tf_decorator.unwrap(object)[1])


def ismethod(object):
    """TFDecorator-aware replacement for inspect.ismethod."""
    return _inspect.ismethod(tf_decorator.unwrap(object)[1])


def ismodule(object):
    """TFDecorator-aware replacement for inspect.ismodule."""
    return _inspect.ismodule(tf_decorator.unwrap(object)[1])


def isroutine(object):
    """TFDecorator-aware replacement for inspect.isroutine."""
    return _inspect.isroutine(tf_decorator.unwrap(object)[1])


def stack(context=1):
    """TFDecorator-aware replacement for inspect.stack."""
    return _inspect.stack(context)[1:]