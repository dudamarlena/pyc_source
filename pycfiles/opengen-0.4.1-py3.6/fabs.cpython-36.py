# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/opengen/functions/fabs.py
# Compiled at: 2019-10-16 17:13:36
# Size of source mod 2**32: 266 bytes
import casadi.casadi as cs, numpy as np
from .is_numeric import *
from .is_symbolic import *

def fabs(u):
    if is_numeric(u):
        return np.fabs(u)
    if is_symbolic(u):
        return cs.fabs(u)
    raise Exception('Illegal argument')