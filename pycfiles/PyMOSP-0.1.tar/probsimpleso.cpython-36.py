# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pymoso/problems/probsimpleso.py
# Compiled at: 2019-09-10 14:12:56
# Size of source mod 2**32: 1186 bytes
__doc__ = '\nSummary\n-------\nProvides implementation of the Test Simple SO Problem\nOracle for use in PyMOSO.\n'
from ..chnbase import Oracle

class ProbSimpleSO(Oracle):
    """ProbSimpleSO"""

    def __init__(self, rng):
        self.num_obj = 1
        self.dim = 1
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
        xr = range(-100, 101)
        isfeas = True
        for xi in x:
            if xi not in xr:
                isfeas = False

        obj1 = []
        if isfeas:
            z1 = rng.normalvariate(0, 3)
            obj1 = x[0] ** 2 + z1
        return (isfeas, (obj1,))