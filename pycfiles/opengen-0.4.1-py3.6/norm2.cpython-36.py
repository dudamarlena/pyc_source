# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/opengen/functions/norm2.py
# Compiled at: 2020-03-10 14:23:40
# Size of source mod 2**32: 401 bytes
import casadi.casadi as cs, numpy as np
from .is_numeric import *
from .is_symbolic import *

def norm2(u):
    if isinstance(u, list) and all(is_numeric(x) for x in u) or isinstance(u, np.ndarray):
        return np.linalg.norm(u)
    if is_symbolic(u):
        return cs.norm_2(u)
    raise Exception('Illegal argument')