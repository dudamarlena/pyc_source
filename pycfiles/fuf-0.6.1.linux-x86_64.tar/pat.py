# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/msoucy/.virtualenv/fuf/lib/python2.7/site-packages/fuf/pat.py
# Compiled at: 2014-09-23 17:45:03
"""
pat.py
Matthew Soucy

Framework for pattern matching multimethods
Some implementation details taken from Guido van Rossum's article on multimethods
"""
import sys
from inspect import isclass, isroutine

def try_pred(pred, arg):
    """ Perform the correct test depending on the type """
    if isclass(pred):
        return isinstance(arg, pred)
    else:
        if isroutine(pred):
            return pred(arg)
        return pred == arg


class OverloadSet(object):
    """ Set of overloaded functions
    Overloads are based on arbitrary constraints """

    def __init__(self):
        """ Initialize an overload set """
        self._overloads = []

    def __call__(self, *args, **kwargs):
        """ Search for the best overload """
        for cond, kcond, func in self._overloads:
            if len(cond) <= len(args) and all(try_pred(c, arg) for c, arg in zip(cond, args)) and all(name in kwargs for name in kcond) and all(kcond[name](kwargs[name]) for name in kcond):
                return func(*args, **kwargs)

        raise RuntimeError('No match found for arguments %s %s' % (args, kwargs))

    def reg(self, *cond, **kwcond):
        """ Registration decorator
        Provides a method to register a function """

        def wrap(f):
            self._overloads.append((cond, kwcond, f))
            return self

        return wrap


def Overload(*constraints, **kconstraints):

    def wrap(f):
        f = getattr(f, '__lastreg__', f)
        name = f.__name__
        mod = sys.modules[f.__module__]
        if not hasattr(mod, name):
            setattr(mod, name, OverloadSet())
        newfunc = getattr(mod, name)
        newfunc.reg(*constraints, **kconstraints)(f)
        newfunc.__lastreg__ = f
        return newfunc

    return wrap