# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../../OrthNet/orthnet/poly/legendre.py
# Compiled at: 2018-03-09 21:14:30
# Size of source mod 2**32: 741 bytes
import tensorflow as tf, torch
from ..utils.poly import Poly1d, Poly

class Legendre(Poly):

    def __init__(self, module, degree, x):
        if module == 'tensorflow':
            initial = [
             lambda x: tf.ones_like(x), lambda x: x]
            recurrence = lambda p1, p2, n, x: ((2 * n + 1) * tf.multiply(x, p1) - n * p2) / (n + 1)
        else:
            if module == 'pytorch':
                initial = [
                 lambda x: torch.ones_like(x), lambda x: x]
                recurrence = lambda p1, p2, n, x: ((2 * n + 1) * x * p1 - n * p2) / (n + 1)
        Poly.__init__(module, degree, x, initial, recurrence)