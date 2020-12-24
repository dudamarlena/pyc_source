# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/pytransit/lpf/tessoclttvlpf.py
# Compiled at: 2020-01-13 18:32:58
# Size of source mod 2**32: 3050 bytes
from pathlib import Path
from astropy.table import Table
from numba import njit, prange
from numpy import atleast_2d, zeros, log, concatenate, pi, transpose, sum, compress, ones
from uncertainties import UFloat, ufloat
from .oclttvlpf import OCLTTVLPF
from utils.keplerlc import KeplerLC
from baselines.legendrebaseline import LegendreBaseline

@njit(parallel=True, cache=False, fastmath=True)
def lnlike_normal_v(o, m, e):
    m = atleast_2d(m)
    npv = m.shape[0]
    npt = o.size
    lnl = zeros(npv)
    for i in prange(npv):
        lnl[i] = -npt * log(e[(i, 0)]) - 0.5 * log(2 * pi) - 0.5 * sum(((o - m[i, :]) / e[(i, 0)]) ** 2)

    return lnl


class TESSCLTTVLPF(LegendreBaseline, OCLTTVLPF):

    def __init__(self, name: str, dfile: Path, zero_epoch: float, period: float, nsamples: int=10, trdur: float=0.125, bldur: float=0.3, nlegendre: int=2, ctx=None, queue=None):
        zero_epoch = zero_epoch if isinstance(zero_epoch, UFloat) else ufloat(zero_epoch, 1e-05)
        period = period if isinstance(period, UFloat) else ufloat(period, 1e-07)
        tb = Table.read(dfile)
        self.bjdrefi = tb.meta['BJDREFI']
        zero_epoch = zero_epoch - self.bjdrefi
        df = tb.to_pandas().dropna(subset=['TIME', 'SAP_FLUX', 'PDCSAP_FLUX'])
        self.lc = lc = KeplerLC(df.TIME.values, df.SAP_FLUX.values, zeros(df.shape[0]), zero_epoch.n, period.n, trdur, bldur)
        LegendreBaseline.__init__(self, nlegendre)
        OCLTTVLPF.__init__(self, name, zero_epoch, period, ['TESS'], times=(lc.time_per_transit),
          fluxes=(lc.normalized_flux_per_transit),
          pbids=(zeros(lc.nt, 'int')),
          nsamples=nsamples,
          exptimes=[0.00139],
          cl_ctx=ctx,
          cl_queue=queue)
        self.lnlikelihood = self.lnlikelihood_nb

    def create_pv_population(self, npop=50):
        pvp = self.ps.sample_from_prior(npop)
        return pvp

    def flux_model(self, pvp):
        tmodel = transpose(self.transit_model(pvp, copy=True)).copy()
        return tmodel * self.baseline(pvp)

    def lnlikelihood_nb(self, pvp):
        fmodel = self.flux_model(pvp).astype('d')
        err = 10 ** atleast_2d(pvp)[:, self._sl_err]
        return lnlike_normal_v(self.ofluxa, fmodel, err)