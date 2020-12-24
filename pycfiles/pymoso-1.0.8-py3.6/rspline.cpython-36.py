# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pymoso/solvers/rspline.py
# Compiled at: 2019-03-26 14:59:03
# Size of source mod 2**32: 1465 bytes
"""
Summary
-------
Provide an implementation of R-SPLINE for users needing a 
single-objective simulation optimization solver. 
"""
from ..chnbase import RASolver
import sys

class RSPLINE(RASolver):
    __doc__ = '\n    R-SPLINE solver for single-objective simulation optimization.\n    \n    Parameters\n    ----------\n    orc : chnbase.Oracle object\n\tkwargs : dict\n\t\n\tSee also\n\t--------\n\tchnbase.RASolver\n    '

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