# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/notekeras/activations/gelu_fallback.py
# Compiled at: 2019-11-22 04:05:10
# Size of source mod 2**32: 182 bytes
import math
import notekeras.backend as K
__all__ = [
 'gelu']

def gelu(x):
    return 0.5 * x * (1.0 + K.tanh(math.sqrt(2.0 / math.pi) * (x + 0.044715 * x * x * x)))