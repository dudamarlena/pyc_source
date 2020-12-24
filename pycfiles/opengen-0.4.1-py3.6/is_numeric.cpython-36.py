# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/opengen/functions/is_numeric.py
# Compiled at: 2019-10-16 17:13:36
# Size of source mod 2**32: 110 bytes
import numpy as np

def is_numeric(u):
    return isinstance(u, (int, float)) or np.isscalar(u)