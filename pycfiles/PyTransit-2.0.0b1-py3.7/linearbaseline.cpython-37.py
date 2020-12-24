# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/pytransit/lpf/baselines/linearbaseline.py
# Compiled at: 2020-03-16 19:34:28
# Size of source mod 2**32: 2887 bytes
from numba import prange, njit
from numpy import atleast_2d, zeros, dot, array, concatenate, squeeze, r_, inf
from ...param import LParameter, NormalPrior as NP

@njit(parallel=True)
def linear_model(pvp, timea, lcids, cstart, ncov, cova):
    pvp = atleast_2d(pvp)
    npv = pvp.shape[0]
    npt = timea.size
    bl = zeros((npv, npt))
    for ipv in prange(npv):
        ii = 0
        for ipt in range(npt):
            ilc = lcids[ipt]
            cst = cstart[ilc]
            nc = ncov[ilc]
            bl[(ipv, ipt)] = pvp[(ipv, cst)] + dot(pvp[ipv, cst + 1:cst + nc], cova[ii:ii + nc - 1])
            ii += nc

    return bl


class LinearModelBaseline:

    def _init_p_baseline(self):
        """Baseline parameter initialisation.
        """
        self.ncov = array([c.shape[1] for c in self.covariates])
        self.cova = concatenate([c.ravel() for c in self.covariates])
        bls = []
        for i, tn in enumerate(range(self.nlc)):
            ins = '' if not hasattr(self, 'ins') else self.ins[i] + '_'
            pii = '' if not hasattr(self, 'piis') else self.piis[i]
            fstd = self.fluxes[i].std()
            bls.append(LParameter(f"bli_{ins}{pii}", f"bl_intercept_{ins}{pii}", '', (NP(1.0, fstd)), bounds=(-inf, inf)))
            for ipoly in range(1, self.ncov[i] + 1):
                bls.append(LParameter(f"bls_{ins}{pii}_{ipoly}", f"bl_c_{ins}{pii}_{ipoly}", '', (NP(0.0, fstd)), bounds=(-inf, inf)))

        self.ps.add_global_block('baseline', bls)
        self._sl_bl = self.ps.blocks[(-1)].slice
        self._start_bl = self.ps.blocks[(-1)].start
        self._bl_coeff_start = r_[([0], self.ncov + 1)].cumsum()

    def baseline(self, pvp):
        pvp = atleast_2d(pvp)
        return squeeze(linear_model(pvp[:, self._sl_bl], self.timea, self.lcids, self._bl_coeff_start, self.ncov, self.cova))