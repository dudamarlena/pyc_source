# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/opengen/functions/sign.py
# Compiled at: 2020-05-07 20:26:31
# Size of source mod 2**32: 264 bytes
import casadi.casadi as cs, numpy as np
from .is_numeric import is_numeric
from .is_symbolic import is_symbolic

def sign(u):
    if is_numeric(u):
        return np.sign(u)
    if is_symbolic(u):
        return cs.sign(u)
    Exception('Illegal argument')