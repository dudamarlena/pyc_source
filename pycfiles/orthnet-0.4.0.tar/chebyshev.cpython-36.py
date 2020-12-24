# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../../OrthNet/orthnet/poly/chebyshev.py
# Compiled at: 2018-04-12 14:35:14
# Size of source mod 2**32: 1727 bytes
import tensorflow as tf, torch, numpy as np
from .poly import Poly

class Chebyshev(Poly):
    __doc__ = '\n\tChebyshev Polynomials of the first kind\n\t'

    def __init__(self, module, degree, x, *args, **kw):
        """
                input:
                        module: ['tensorflow', 'torch', 'numpy']
                        degree: highest degree of polynomial
                        x: a tensor of shape [Nsample*Nparameter], each row is a sample point, each column represents a parameter
                """
        if module == 'tensorflow':
            initial = [
             lambda x: tf.ones_like(x), lambda x: x]
            recurrence = lambda p1, p2, n, x: 2 * tf.multiply(x, p1) - p2
        else:
            if module == 'torch':
                initial = [
                 lambda x: torch.ones_like(x), lambda x: x]
                recurrence = lambda p1, p2, n, x: x * p1 * 2 - p2
            else:
                if module == 'numpy':
                    initial = [
                     lambda x: np.ones_like(x), lambda x: x]
                    recurrence = lambda p1, p2, n, x: 2 * x * p1 - p2
        (Poly.__init__)(self, module, degree, x, initial, recurrence, *args, **kw)


class Chebyshev2(Poly):
    __doc__ = '\n\tChebyshev Polynomials of the second kind\n\t'

    def __init__(self, module, degree, x, *args, **kw):
        """
                input:
                        module: ['tensorflow', 'torch', 'numpy']
                        degree: highest degree of polynomial
                        x: a tensor of shape [Nsample*Nparameter], each row is a sample point, each column represents a parameter
                """
        if module == 'tensorflow':
            initial = [
             lambda x: tf.ones_like(x), lambda x: 2 * x]
            recurrence = lambda p1, p2, n, x: 2 * tf.multiply(x, p1) - p2
        else:
            if module == 'torch':
                initial = [
                 lambda x: torch.ones_like(x), lambda x: x * 2]
                recurrence = lambda p1, p2, n, x: x * p1 * 2 - p2
            else:
                if module == 'numpy':
                    initial = [
                     lambda x: np.ones_like(x), lambda x: 2 * x]
                    recurrence = lambda p1, p2, n, x: 2 * x * p1 - p2
        (Poly.__init__)(self, module, degree, x, initial, recurrence, *args, **kw)