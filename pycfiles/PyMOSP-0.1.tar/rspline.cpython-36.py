# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pymoso/solvers/rspline.py
# Compiled at: 2019-03-26 14:59:03
# Size of source mod 2**32: 1465 bytes
__doc__ = '\nSummary\n-------\nProvide an implementation of R-SPLINE for users needing a \nsingle-objective simulation optimization solver. \n'
from ..chnbase import RASolver
import sys

class RSPLINE(RASolver):
    """RSPLINE"""

    def __init__(self, orc, **kwargs):
        if orc.num_obj > 1:
            print('--* Warning: R-SPLINE operates on single objective problems!')
            print('--* Continuing: R-SPLINE will optimize only the first objective.')
        (super().__init__)(orc, **kwargs)

    def spsolve(self, warm_start):
        """
        Use SPLINE to solve the sample path problem. 
        
        Parameters
        ----------
        warm_start : set of tuple of int
                        For RSPLINE, this is a singleton set
                
                Returns
                -------
                set of tuple of int
                        For RSPLINE, this is a singleton set containing the sample
                        path minimizer
        """
        warm_start = self.upsample(warm_start)
        if not warm_start:
            print('--* R-SPLINE Error: Empty warm start. Is x0 feasible?')
            print('--* Aborting. ')
            sys.exit()
        ws = warm_start.pop()
        _, xmin, _, _ = self.spline(ws)
        return {
         xmin}