# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\cgp\examples\sensitivity_beeler.py
# Compiled at: 2013-01-14 06:47:43
"""Sensitivity analysis of action potential duration, bridging R and Python."""
import numpy as np, rpy2.rinterface as ri
from cgp.utils.rnumpy import r, py2ri
from joblib import Memory
from cgp.physmod.cellmlmodel import Cellmlmodel
from cgp.phenotyping.attractor import AttractorMixin
from cgp.virtexp.elphys.clampable import Clampable
from cgp.virtexp.elphys.paceable import Paceable
from cgp.virtexp.elphys.paceable import ap_stats_array
from cgp.utils.unstruct import unstruct
from cgp.utils.failwith import failwithnanlikefirst
if __name__ == '__main__':
    r.library('sensitivity')
mem = Memory('/tmp/sensitivity_beeler')

class Model(Cellmlmodel, Clampable, Paceable, AttractorMixin):
    """Mix and match virtual experiments."""
    pass


m = Model(workspace='beeler_reuter_1977', rename=dict(p=dict(IstimPeriod='stim_period', IstimAmplitude='stim_amplitude', IstimPulseDuration='stim_duration')), reltol=1e-10, maxsteps=1000000.0, chunksize=100000)
m.pr.IstimStart = 0
factors = [ k for k in m.dtype.p.names if m.pr[k] != 0 ]

@mem.cache
@failwithnanlikefirst
def phenotypes(par=None):
    """Aggregate phenotypes for sensitivity analysis."""
    with m.autorestore(_p=par):
        m.eq(tmax=10000.0, tol=0.001)
        _t, _y, stats = m.ap()
    return ap_stats_array(stats)


phenotypes()

def mat2par(mat):
    """Make parameter recarray from R matrix."""
    mat = np.copy(mat)
    par = np.tile(m.pr, len(mat))
    for i, factor in enumerate(factors):
        par[factor] = mat[:, i]

    return par


def scalar_pheno(field):
    """Make a function to return a named field of the phenotype array."""

    @ri.rternalize
    def fun(rmatrix):
        """Scalar function for use with R's sensitivity::morris()."""
        ph = np.concatenate([ phenotypes(i) for i in mat2par(rmatrix) ])
        return py2ri(ph[field])

    return fun


if __name__ == '__main__':
    baseline = unstruct(m.pr[factors])
    lower = 0.5 * baseline
    upper = 1.5 * baseline
    result = dict()
    for field in ('appeak', 'apd90', 'ctpeak', 'ctbase', 'ctd90'):
        r.set_seed(20120221)
        result[field] = r.morris(scalar_pheno(field), factors=factors, r=2, design={'type': 'oat', 'levels': 10, 'grid.jump': 5}, binf=lower, bsup=upper)

    r.png('sensitivity.png', width=1024, height=768, pointsize=24)
    r.par(mfrow=(2, 3))
    for k, v in result.items():
        print '===================================================='
        print k
        print v
        r.plot(v, log='y', main=k)

    r.dev_off()