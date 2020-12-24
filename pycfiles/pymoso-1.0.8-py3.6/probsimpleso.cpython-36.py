# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pymoso/problems/probsimpleso.py
# Compiled at: 2019-09-10 14:12:56
# Size of source mod 2**32: 1186 bytes
"""
Summary
-------
Provides implementation of the Test Simple SO Problem
Oracle for use in PyMOSO.
"""
from ..chnbase import Oracle

class ProbSimpleSO(Oracle):
    __doc__ = '\n    An Oracle that simulates the Test Simple SO problem.\n\n    Attributes\n    ----------\n    num_obj : int, 1\n    dim : int, 1\n\n    Parameters\n    ----------\n    rng : prng.MRG32k3a object\n\n    See also\n    --------\n    chnbase.Oracle\n    '

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
        return (
         isfeas, (obj1,))