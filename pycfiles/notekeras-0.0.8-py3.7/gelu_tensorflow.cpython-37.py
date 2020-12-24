# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/notekeras/activations/gelu_tensorflow.py
# Compiled at: 2019-11-22 03:19:58
# Size of source mod 2**32: 136 bytes
from tensorflow.python.ops.math_ops import erf, sqrt
__all__ = ['gelu']

def gelu(x):
    return 0.5 * x * (1.0 + erf(x / sqrt(2.0)))