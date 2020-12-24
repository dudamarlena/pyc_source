# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pymoso/problems/probtpc.py
# Compiled at: 2019-09-10 14:13:08
# Size of source mod 2**32: 1709 bytes
__doc__ = '\nSummary\n-------\nProvides implementation of the Test Problem C Oracle for use in PyMOSO.\n'
from ..chnbase import Oracle
from math import exp, sqrt, sin

class ProbTPC(Oracle):
    """ProbTPC"""

    def __init__(self, rng):
        self.num_obj = 2
        self.dim = 3
        self.density_factor = 2
        super().__init__(rng)

    def g(self, x, rng):
        """
        Simulates one replication. PyMOSO requires that all valid
        Oracles implement an Oracle.g.

        Parameters
        ----------
        x : tuple of int
        rng : prng.MRG32k3a object

        Returns
        -------
        isfeas : bool
        tuple of float
            simulated objective values
        """
        df = self.density_factor
        xr = range(-5 * df, 5 * df + 1)
        obj1 = None
        obj2 = None
        isfeas = True
        for xi in x:
            if xi not in xr:
                isfeas = False

        if isfeas:
            z1 = rng.normalvariate(0, 1)
            z2 = rng.normalvariate(0, 1)
            z3 = rng.normalvariate(0, 1)
            xi = (z1 ** 2, z2 ** 2, z3 ** 2)
            x = tuple(i / df for i in x)
            s = [sin(i) for i in x]
            sum1 = [-10 * xi[i] * exp(-0.2 * sqrt(x[i] ** 2 + x[(i + 1)] ** 2)) for i in (0,
                                                                                          1)]
            sum2 = [xi[i] * (pow(abs(x[i]), 0.8) + 5 * pow(s[i], 3)) for i in (0, 1,
                                                                               2)]
            obj1 = sum(sum1)
            obj2 = sum(sum2)
        return (isfeas, (obj1, obj2))