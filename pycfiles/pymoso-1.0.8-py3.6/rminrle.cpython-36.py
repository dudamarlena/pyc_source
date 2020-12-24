# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pymoso/solvers/rminrle.py
# Compiled at: 2019-03-26 15:36:40
# Size of source mod 2**32: 843 bytes
"""
Summary
-------
Provide an implementation of R-MinRLE for users needing a
multi-objective simulation optimization solver.
"""
from ..chnbase import RLESolver
import sys

class RMINRLE(RLESolver):
    __doc__ = '\n    A solver using R-MinRLE for integer-ordered MOSO.\n\n    See also\n    --------\n    chnbase.RLESolver\n    '

    def accel(self, warm_start):
        """
        Compute a candidate ALES. RLESolvers require that this function
        is implemented.

        Parameters
        ----------
        warm_start : set of tuple of int

        Returns
        -------
        set of tuple of int
        """
        if not warm_start:
            print('--* R-MinRLE Error: No feasible warm start. Is x0 feasible?')
            print('--* Aborting.')
            sys.exit()
        return self.get_min(warm_start)