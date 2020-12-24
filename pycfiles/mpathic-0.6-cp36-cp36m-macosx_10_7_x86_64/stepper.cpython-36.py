# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tareen/Desktop/Desktop_Tests/MPathic/mpathic/src/stepper.py
# Compiled at: 2018-04-04 08:33:33
# Size of source mod 2**32: 1690 bytes
import pymc, scipy as sp

class MatColumnMetropolis(pymc.Metropolis):

    def __init__(self, stochastic):
        pymc.Metropolis.__init__(self, stochastic)

    def propose(self):
        sigma = 0.5 * self.adaptive_scale_factor
        j_p = sp.random.randint(self.stochastic.value.shape[1])
        emat_temp = self.stochastic.value.copy()
        emat_temp[:, j_p] = emat_temp[:, j_p] + sigma * sp.randn(4)
        self.stochastic.value = emat_temp


class GaugePreservingStepper(pymc.Metropolis):
    __doc__ = 'Perform monte carlo steps that preserve the following choise of gauge:\n    sum of elements in each column = 0, overall matrix norm = 1.'

    def __init__(self, stochastic):
        pymc.Metropolis.__init__(self, stochastic)

    def propose(self):
        emat_temp = self.stochastic.value.copy()
        num_col = emat_temp.shape[1]
        r = sp.random.standard_normal(emat_temp.shape)
        lambda_0 = sp.sum(emat_temp * r)
        lambda_vec = 0.5 * sp.sum(r, axis=0)
        s = sp.zeros_like(r)
        for j in range(emat_temp.shape[1]):
            s[:, j] = r[:, j] - lambda_0 * emat_temp[:, j] - lambda_vec[j] * (0.5 * sp.ones(emat_temp.shape[0]))

        dx = self.adaptive_scale_factor * s / sp.sqrt(sp.sum(s * s))
        self.stochastic.value = (emat_temp + dx) / sp.sqrt(sp.sum((emat_temp + dx) ** 2))