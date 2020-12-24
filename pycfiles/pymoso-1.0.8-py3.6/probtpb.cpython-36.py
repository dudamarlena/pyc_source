# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pymoso/problems/probtpb.py
# Compiled at: 2019-09-10 14:13:04
# Size of source mod 2**32: 1652 bytes
"""
Summary
-------
Provides implementation of the Test Problem B Oracle for use in PyMOSO.
"""
from ..chnbase import Oracle
from math import exp

class ProbTPB(Oracle):
    __doc__ = '\n    An Oracle that simulates Test Problem B.\n\n    Attributes\n    ----------\n    num_obj : int, 2\n    dim : int, 2\n\n    Parameters\n    ----------\n    rng : prng.MRG32k3a object\n\n    See also\n    --------\n    chnbase.Oracle\n    '

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
        return (
         isfeas, (obj1, obj2))