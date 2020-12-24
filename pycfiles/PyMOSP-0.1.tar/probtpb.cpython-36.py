# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pymoso/problems/probtpb.py
# Compiled at: 2019-09-10 14:13:04
# Size of source mod 2**32: 1652 bytes
__doc__ = '\nSummary\n-------\nProvides implementation of the Test Problem B Oracle for use in PyMOSO.\n'
from ..chnbase import Oracle
from math import exp

class ProbTPB(Oracle):
    """ProbTPB"""

    def __init__(self, rng):
        self.num_obj = 2
        self.dim = 2
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
        obj1 = None
        obj2 = None
        isfeas = True
        xr = range(0, 101)
        for xi in x:
            if xi not in xr:
                isfeas = False

        if isfeas:
            z1 = rng.normalvariate(0, 1)
            z2 = rng.normalvariate(0, 1)
            xi = (z1 ** 2, z2 ** 2)
            g1 = 4 * x[0] / 100
            if x[1] >= 0:
                if x[1] <= 40:
                    f2 = 4 - 3 * exp(-pow((x[1] - 20) / 2, 2))
            else:
                f2 = 4 - 2 * exp(-pow((x[1] - 70) / 20, 2))
            alpha = 0.25 + 3.75 * (f2 - 1)
            if g1 <= f2:
                h = 1 - pow(g1 / f2, alpha)
            else:
                h = 0
            obj2 = xi[0] * g1
            obj1 = xi[0] * xi[1] * f2 * h
        return (isfeas, (obj1, obj2))