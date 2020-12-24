# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xpython/buildclass.py
# Compiled at: 2020-05-07 08:09:19
from xpython.pyobj import Function, Cell

def build_class(func, name, *bases, **kwds):
    """
    Like built-in __build_class__() in bltinmodule.c, but running in the
    byterun VM.
    """
    if not isinstance(func, Function):
        raise TypeError('func must be a function')
    if not isinstance(name, str):
        raise TypeError('name is not a string')
    metaclass = kwds.pop('metaclass', None)
    if metaclass is None:
        metaclass = type(bases[0]) if bases else type
    if isinstance(metaclass, type):
        metaclass = calculate_metaclass(metaclass, bases)
    if hasattr(metaclass, '__prepare__'):
        prepare = metaclass.__prepare__
        namespace = prepare(name, bases, **kwds)
    else:
        namespace = {}
    frame = func._vm.make_frame(code=func.func_code, f_globals=func.func_globals, f_locals=namespace)
    cell = func._vm.run_frame(frame)
    cls = metaclass(name, bases, namespace)
    if isinstance(cell, Cell):
        cell.set(cls)
    return cls


def calculate_metaclass(metaclass, bases):
    """Determine the most derived metatype."""
    winner = metaclass
    for base in bases:
        t = type(base)
        if issubclass(t, winner):
            winner = t
        elif not issubclass(winner, t):
            raise TypeError('metaclass conflict', winner, t)

    return winner