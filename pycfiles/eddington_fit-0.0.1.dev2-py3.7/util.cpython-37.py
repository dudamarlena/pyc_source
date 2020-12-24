# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eddington_fit/util.py
# Compiled at: 2020-04-20 10:00:06
# Size of source mod 2**32: 128 bytes
import numpy as np

def get_a0(n, a0=None):
    if a0 is not None:
        return a0
    return np.full(shape=n, fill_value=1)