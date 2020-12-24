# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../../OrthNet/orthnet/poly/legendre.py
# Compiled at: 2018-04-12 14:35:14
# Size of source mod 2**32: 2034 bytes
import tensorflow as tf, torch, numpy as np
from .poly import Poly

class Legendre(Poly):
    __doc__ = '\n\tLegendre Polynomials\n\t'

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
            recurrence = lambda p1, p2, n, x: ((2 * n + 1) * tf.multiply(x, p1) - n * p2) / (n + 1)
        else:
            if module == 'torch':
                initial = [
                 lambda x: torch.ones_like(x), lambda x: x]
                recurrence = lambda p1, p2, n, x: (x * p1 * (2 * n + 1) - p2 * n) / (n + 1)
            else:
                if module == 'numpy':
                    initial = [
                     lambda x: np.ones_like(x), lambda x: x]
                    recurrence = lambda p1, p2, n, x: ((2 * n + 1) * x * p1 - n * p2) / (n + 1)
        (Poly.__init__)(self, module, degree, x, initial, recurrence, *args, **kw)


class Legendre_Normalized(Poly):
    __doc__ = '\n\tNormalized Legendre Polynomials with inner product be 1 if n = m.\n\t'

    def __init__(self, module, degree, x, *args, **kw):
        """
                input:
                        module: ['tensorflow', 'torch', 'numpy']
                        degree: highest degree of polynomial
                        x: a tensor of shape [Nsample*Nparameter], each row is a sample point, each column represents a parameter
                """
        if module == 'tensorflow':
            initial = [
             lambda x: tf.ones_like(x) * np.sqrt(0.5), lambda x: x * np.sqrt(1.5)]
            recurrence = lambda p1, p2, n, x: (np.sqrt((2 * n + 1) * (2 * n + 3)) * tf.multiply(x, p1) - n * np.sqrt((2 * n + 3) / (2 * n - 1)) * p2) / (n + 1)
        else:
            if module == 'torch':
                initial = [
                 lambda x: torch.ones_like(x) * np.sqrt(0.5), lambda x: x * np.sqrt(1.5)]
                recurrence = lambda p1, p2, n, x: (x * p1 * np.sqrt((2 * n + 1) * (2 * n + 3)) - p2 * n * np.sqrt((2 * n + 3) / (2 * n - 1))) / (n + 1)
            else:
                if module == 'numpy':
                    initial = [
                     lambda x: np.ones_like(x) * np.sqrt(0.5), lambda x: x * np.sqrt(1.5)]
                    recurrence = lambda p1, p2, n, x: (np.sqrt((2 * n + 1) * (2 * n + 3)) * x * p1 - n * np.sqrt((2 * n + 3) / (2 * n - 1)) * p2) / (n + 1)
        (Poly.__init__)(self, module, degree, x, initial, recurrence, *args, **kw)