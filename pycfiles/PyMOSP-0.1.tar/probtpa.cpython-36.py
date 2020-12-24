# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pymoso/problems/probtpa.py
# Compiled at: 2019-09-10 14:13:50
# Size of source mod 2**32: 1407 bytes
__doc__ = '\nSummary\n-------\nProvides implementation of the Test Problem A Oracle for use in PyMOSO.\n'
from ..chnbase import Oracle

class ProbTPA(Oracle):
    """ProbTPA"""

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
        xr = range(0, 51)
        isfeas = True
        for xi in x:
            if xi not in xr:
                isfeas = False

        obj1 = None
        obj2 = None
        if isfeas:
            z1 = rng.normalvariate(0, 1)
            z2 = rng.normalvariate(0, 1)
            z3 = rng.normalvariate(0, 1)
            xi = [z1 ** 2, z2 ** 2, z3 ** 2]
            obj1 = (x[0] / 10.0 - 2.0 * xi[0]) ** 2 + (x[1] / 10.0 - xi[1]) ** 2
            obj2 = x[0] ** 2 / 100.0 + (x[1] / 10.0 - 2.0 * xi[2]) ** 2
        return (isfeas, (obj1, obj2))