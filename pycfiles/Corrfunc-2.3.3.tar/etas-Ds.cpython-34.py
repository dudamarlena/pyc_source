# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/gpl/software/python/corrfitter/examples/etas-Ds.py
# Compiled at: 2017-02-13 12:39:10
# Size of source mod 2**32: 5325 bytes
from __future__ import print_function
import collections, sys, h5py, gvar as gv, numpy as np, corrfitter as cf
SHOWPLOTS = True

def main():
    data = make_data('etas-Ds.h5')
    fitter = cf.CorrFitter(models=make_models(), svdcut=1e-05)
    p0 = None
    for N in [1, 2, 3, 4]:
        print(30 * '=', 'nterm =', N)
        prior = make_prior(N)
        fit = fitter.lsqfit(data=data, prior=prior, p0=p0)
        print(fit.format(pstyle=None if N < 4 else 'v'))
        p0 = fit.pmean

    print_results(fit, prior, data)
    if SHOWPLOTS:
        fit.show_plots()
    test_fit(fitter, 'etas-Ds.h5')


def test_fit(fitter, datafile):
    """ Test the fit with simulated data """
    gv.ranseed(98)
    print('\nRandom seed:', gv.ranseed.seed)
    dataset = h5py.File(datafile)
    pexact = fitter.fit.pmean
    prior = fitter.fit.prior
    for spdata in fitter.simulated_pdata_iter(n=2, dataset=dataset, pexact=pexact):
        print('\n============================== simulation')
        sfit = fitter.lsqfit(pdata=spdata, prior=prior, p0=pexact)
        print(sfit.format(pstyle=None))
        diff = {}
        for k in ['etas:a', 'etas:dE', 'Ds:a', 'Ds:dE', 'Vnn']:
            p_k = sfit.p[k].flat[0]
            pex_k = pexact[k].flat[0]
            print('{:>10}:  fit = {}    exact = {:<9.5}    diff = {}'.format(k, p_k, pex_k, p_k - pex_k))
            diff[k] = p_k - pex_k

        print('\nAccuracy of key parameters: ' + gv.fmt_chi2(gv.chi2(diff)))


def make_data(datafile):
    """ Read data from datafile and average it. """
    dset = cf.read_dataset(datafile)
    return gv.dataset.avg_data(dset)


def make_models():
    """ Create models to fit data. """
    tmin = 5
    tp = 64
    models = [
     cf.Corr2(datatag='etas', tp=tp, tmin=tmin, a='etas:a', b='etas:a', dE='etas:dE'),
     cf.Corr2(datatag='Ds', tp=tp, tmin=tmin, a=('Ds:a', 'Dso:a'), b=('Ds:a', 'Dso:a'), dE=('Ds:dE',
                                                                                       'Dso:dE')),
     cf.Corr3(datatag='3ptT15', T=15, tmin=tmin, a='etas:a', dEa='etas:dE', b=('Ds:a', 'Dso:a'), dEb=('Ds:dE',
                                                                                                 'Dso:dE'), Vnn='Vnn', Vno='Vno'),
     cf.Corr3(datatag='3ptT16', T=16, tmin=tmin, a='etas:a', dEa='etas:dE', b=('Ds:a', 'Dso:a'), dEb=('Ds:dE',
                                                                                                 'Dso:dE'), tpb=tp, Vnn='Vnn', Vno='Vno')]
    return models


def make_prior(N):
    """ Create priors for fit parameters. """
    prior = gv.BufferDict()
    metas = gv.gvar('0.4(2)')
    prior['log(etas:a)'] = gv.log(gv.gvar(N * ['0.3(3)']))
    prior['log(etas:dE)'] = gv.log(gv.gvar(N * ['0.5(5)']))
    prior['log(etas:dE)'][0] = gv.log(metas)
    mDs = gv.gvar('1.2(2)')
    prior['log(Ds:a)'] = gv.log(gv.gvar(N * ['0.3(3)']))
    prior['log(Ds:dE)'] = gv.log(gv.gvar(N * ['0.5(5)']))
    prior['log(Ds:dE)'][0] = gv.log(mDs)
    prior['log(Dso:a)'] = gv.log(gv.gvar(N * ['0.1(1)']))
    prior['log(Dso:dE)'] = gv.log(gv.gvar(N * ['0.5(5)']))
    prior['log(Dso:dE)'][0] = gv.log(mDs + gv.gvar('0.3(3)'))
    prior['Vnn'] = gv.gvar(N * [N * ['0(1)']])
    prior['Vno'] = gv.gvar(N * [N * ['0(1)']])
    return prior


def print_results(fit, prior, data):
    """ Report best-fit results. """
    print('Fit results:')
    p = fit.p
    E_etas = np.cumsum(p['etas:dE'])
    a_etas = p['etas:a']
    print('  Eetas:', E_etas[:3])
    print('  aetas:', a_etas[:3])
    E_Ds = np.cumsum(p['Ds:dE'])
    a_Ds = p['Ds:a']
    print('\n  EDs:', E_Ds[:3])
    print('  aDs:', a_Ds[:3])
    E_Dso = np.cumsum(p['Dso:dE'])
    a_Dso = p['Dso:a']
    print('\n  EDso:', E_Dso[:3])
    print('  aDso:', a_Dso[:3])
    Vnn = p['Vnn']
    Vno = p['Vno']
    print('\n  etas->V->Ds  =', Vnn[(0, 0)])
    print('  etas->V->Dso =', Vno[(0, 0)])
    outputs = collections.OrderedDict()
    outputs['metas'] = E_etas[0]
    outputs['mDs'] = E_Ds[0]
    outputs['mDso-mDs'] = E_Dso[0] - E_Ds[0]
    outputs['Vnn'] = Vnn[(0, 0)]
    outputs['Vno'] = Vno[(0, 0)]
    inputs = collections.OrderedDict()
    inputs['statistics'] = data
    inputs.update(prior)
    inputs['svd'] = fit.svdcorrection
    print('\n' + gv.fmt_values(outputs))
    print(gv.fmt_errorbudget(outputs, inputs))
    print('\n')


if sys.argv[1:]:
    SHOWPLOTS = eval(sys.argv[1])
if SHOWPLOTS:
    try:
        import matplotlib
    except ImportError:
        SHOWPLOTS = False

if __name__ == '__main__':
    main()