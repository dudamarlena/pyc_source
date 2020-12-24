# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pymoso/problems/probtpa.py
# Compiled at: 2019-09-10 14:13:50
# Size of source mod 2**32: 1407 bytes
"""
Summary
-------
Provides implementation of the Test Problem A Oracle for use in PyMOSO.
"""
from ..chnbase import Oracle

class ProbTPA(Oracle):
    __doc__ = '\n    An Oracle that simulates Test Problem A.\n\n    Attributes\n    ----------\n    num_obj : int, 2\n    dim : int, 2\n\n    Parameters\n    ----------\n    rng : prng.MRG32k3a object\n\n    See also\n    --------\n    chnbase.Oracle\n    '

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
        return (
         isfeas, (obj1, obj2))