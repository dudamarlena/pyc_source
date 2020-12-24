# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./test_larch_plugin.py
# Compiled at: 2020-01-31 21:40:19
# Size of source mod 2**32: 924 bytes
import numpy as np

def fcn0():
    """0 arg  """
    return True


def fcn1(x):
    """1 arg  """
    return x


def add2(x, y):
    """2 args  """
    return 2 * x + y


def add_scale(x, y, scale=1):
    """2 pos args, 1 var  """
    return (2 * x + y) * scale


def f1_larch(x, option=False):
    """1 arg, with an option="""
    if option:
        return x
    return 2 * x


def f1_kwargs(x, **kws):
    """1 arg, with **kws"""
    if x:
        return 2 * x
    return len(kws)


def f1_varargs(x, *args):
    """1 arg, with *args"""
    print(' f1 varargs ', args, kws)
    return 2 * x


def registerLarchPlugin():
    return (
     '_tests',
     dict(fcn0=fcn0, fcn1=fcn1, add2=add2,
       add_scale=add_scale,
       f1_larch=f1_larch,
       f1_kwargs=f1_kwargs,
       f1_varargs=f1_varargs))