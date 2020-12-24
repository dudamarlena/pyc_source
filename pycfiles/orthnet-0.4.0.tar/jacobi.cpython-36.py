# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../../OrthNet/orthnet/poly/jacobi.py
# Compiled at: 2018-04-12 14:35:14
# Size of source mod 2**32: 1523 bytes
import tensorflow as tf, torch, numpy as np
from .poly import Poly

class Jacobi(Poly):
    __doc__ = '\n\tJacobi Polynomials\n\t'

    def __init__(self, module, degree, x, alpha, beta, *args, **kw):
        """
                input:
                        module: ['tensorflow', 'torch', 'numpy']
                        degree: highest degree of polynomial
                        x: a tensor of shape [Nsample*Nparameter], each row is a sample point, each column represents a parameter
                        alpha, beta: the parameters of Jacobi polynomials
                """
        if module == 'tensorflow':
            initial = [
             lambda x: tf.ones_like(x), lambda x: 0.5 * (alpha + beta + 2) * x + 0.5 * (alpha - beta)]
            recurrence = lambda p1, p2, n, x: ((2 * n + alpha + beta - 1) * tf.multiply((2 * n + alpha + beta) * (2 * n + alpha + beta - 2) * x + alpha ** 2 - beta ** 2, p1) - 2 * (n + alpha - 1) * (n + beta - 1) * (2 * n + alpha + beta) * p2) / (2 * n * (n + alpha + beta) * (2 * n + alpha + beta - 2))
        else:
            if module == 'torch':
                initial = [
                 lambda x: torch.ones_like(x), lambda x: x * 0.5 * (alpha + beta + 2) + 0.5 * (alpha - beta)]
                recurrence = lambda p1, p2, n, x: ((x * (2 * n + alpha + beta) * (2 * n + alpha + beta - 2) + alpha ** 2 - beta ** 2) * p1 * (2 * n + alpha + beta - 1) - (p2 * n + alpha - 1) * (n + beta - 1) * (2 * n + alpha + beta)) * 2 / (2 * n * (n + alpha + beta) * (2 * n + alpha + beta - 2))
            else:
                if module == 'numpy':
                    initial = [
                     lambda x: np.ones_like(x), lambda x: 0.5 * (alpha + beta + 2) * x + 0.5 * (alpha - beta)]
                    recurrence = lambda p1, p2, n, x: ((2 * n + alpha + beta - 1) * ((2 * n + alpha + beta) * (2 * n + alpha + beta - 2) * x + alpha ** 2 - beta ** 2) * p1 - 2 * (n + alpha - 1) * (n + beta - 1) * (2 * n + alpha + beta) * p2) / (2 * n * (n + alpha + beta) * (2 * n + alpha + beta - 2))
        (Poly.__init__)(self, module, degree, x, initial, recurrence, *args, **kw)