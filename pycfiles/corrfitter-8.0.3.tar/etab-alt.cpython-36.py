# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/gpl/software/python/corrfitter/examples/etab-alt.py
# Compiled at: 2019-03-28 06:51:45
# Size of source mod 2**32: 3197 bytes
from __future__ import print_function
import collections, gvar as gv, numpy as np, corrfitter as cf
DISPLAYPLOTS = False
SOURCES = [
 'l', 'g', 'd', 'e']
EIG_SOURCES = ['0', '1', '2', '3']
KEYFMT = '1s0.{s1}{s2}'
TDATA = range(1, 24)
SVDCUT = 0.06
try:
    import matplotlib
except ImportError:
    DISPLAYPLOTS = False

def main():
    data, basis = make_data('etab.h5')
    fitter = cf.CorrFitter(models=(make_models()))
    p0 = None
    for N in range(1, 8):
        print(30 * '=', 'nterm =', N)
        prior = make_prior(N, basis)
        fit = fitter.lsqfit(data=data, prior=prior, p0=p0, svdcut=SVDCUT)
        print(fit.format(pstyle=(None if N < 7 else 'm')))
        p0 = fit.pmean

    print_results(fit, basis, prior, data)
    if DISPLAYPLOTS:
        fitter.display_plots()
    print('\n==================== add svd, prior noise')
    noisy_fit = fitter.lsqfit(data=data,
      prior=prior,
      p0=(fit.pmean),
      svdcut=SVDCUT,
      add_svdnoise=True,
      add_priornoise=True)
    print(noisy_fit.format(pstyle=None))
    dE = fit.p['etab.dE'][:3]
    noisy_dE = noisy_fit.p['etab.dE'][:3]
    print('      dE:', dE)
    print('noisy dE:', noisy_dE)
    print('          ', gv.fmt_chi2(gv.chi2(dE - noisy_dE)))


def make_data(filename):
    data = gv.dataset.avg_data(cf.read_dataset(filename))
    basis = cf.EigenBasis(data,
      keyfmt='1s0.{s1}{s2}', srcs=['l', 'g', 'd', 'e'], t=(1, 2),
      tdata=(range(1, 24)))
    return (
     basis.apply(data, keyfmt='1s0.{s1}{s2}'), basis)


def make_models():
    models = []
    for i, s1 in enumerate(EIG_SOURCES):
        for s2 in EIG_SOURCES[i:]:
            if s1 != s2:
                pass
            else:
                tfit = TDATA if s1 == s2 else TDATA[:12]
                otherdata = None if s1 == s2 else KEYFMT.format(s1=s2, s2=s1)
                models.append(cf.Corr2(datatag=KEYFMT.format(s1=s1, s2=s2),
                  tdata=TDATA,
                  tfit=tfit,
                  a=('etab.' + s1),
                  b=('etab.' + s2),
                  dE='etab.dE',
                  otherdata=otherdata))

    return models


def make_prior(N, basis):
    return basis.make_prior(nterm=N, keyfmt='etab.{s1}', eig_srcs=True)


def print_results(fit, basis, prior, data):
    print(30 * '=', 'Results\n')
    print(basis.tabulate((fit.p), keyfmt='etab.{s1}'))
    print(basis.tabulate((fit.p), keyfmt='etab.{s1}', eig_srcs=True))
    E = np.cumsum(fit.p['etab.dE'])
    outputs = collections.OrderedDict()
    outputs['a*E(2s-1s)'] = E[1] - E[0]
    outputs['a*E(3s-1s)'] = E[2] - E[0]
    outputs['E(3s-1s)/E(2s-1s)'] = (E[2] - E[0]) / (E[1] - E[0])
    inputs = collections.OrderedDict()
    inputs['prior'] = prior
    inputs['data'] = data
    inputs['svdcut'] = fit.svdcorrection
    print(gv.fmt_values(outputs))
    print(gv.fmt_errorbudget(outputs, inputs, colwidth=18))


if __name__ == '__main__':
    main()