# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pymoso/solvers/rminrle.py
# Compiled at: 2019-03-26 15:36:40
# Size of source mod 2**32: 843 bytes
__doc__ = '\nSummary\n-------\nProvide an implementation of R-MinRLE for users needing a\nmulti-objective simulation optimization solver.\n'
from ..chnbase import RLESolver
import sys

class RMINRLE(RLESolver):
    """RMINRLE"""

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