# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyproffit/fitting.py
# Compiled at: 2019-11-11 09:06:49
# Size of source mod 2**32: 4448 bytes
import numpy as np, iminuit

class ChiSquared:

    def __init__(self, model, x, y, dy, psfmat=None, fitlow=None, fithigh=None):
        self.model = model
        self.x = x
        self.y = y
        self.dy = dy
        fitl = 0.0
        fith = 10000000000.0
        if fitlow is not None:
            fitl = fitlow
        else:
            if fithigh is not None:
                fith = fithigh
            self.region = np.where(np.logical_and(x >= fitl, x <= fith))
            self.nonz = np.where(dy[self.region] > 0.0)
            if psfmat is not None:
                self.psfmat = psfmat
            else:
                self.psfmat = None
        self.func_code = iminuit.util.make_func_code(iminuit.util.describe(self.model)[1:])

    def __call__(self, *par):
        ym = (self.model)(self.x, *par)
        if self.psfmat is not None:
            ym = np.dot(self.psfmat, ym)
        reg = self.region
        nonz = self.nonz
        chi2 = np.sum((self.y[reg][nonz] - ym[reg][nonz]) ** 2 / self.dy[reg][nonz] ** 2)
        return chi2


class Cstat:

    def __init__(self, model, x, counts, area, effexp, bkgc, psfmat=None, fitlow=None, fithigh=None):
        self.model = model
        self.x = x
        self.c = counts
        self.area = area
        self.effexp = effexp
        self.bkgc = bkgc
        fitl = 0.0
        fith = 10000000000.0
        if fitlow is not None:
            fitl = fitlow
        else:
            if fithigh is not None:
                fith = fithigh
            self.region = np.where(np.logical_and(x >= fitl, x <= fith))
            self.nonz = np.where(counts[self.region] > 0.0)
            self.isz = np.where(counts[self.region] == 0)
            if psfmat is not None:
                self.psfmat = psfmat
            else:
                self.psfmat = None
        self.func_code = iminuit.util.make_func_code(iminuit.util.describe(self.model)[1:])

    def __call__(self, *par):
        ym = (self.model)(self.x, *par)
        modcounts = ym * self.area * self.effexp
        if self.psfmat is not None:
            modcounts = np.dot(self.psfmat, modcounts)
        mm = modcounts + self.bkgc
        reg = self.region
        nc = self.c
        nonz = self.nonz
        cstat = 2.0 * np.sum(mm[reg][nonz] - nc[reg][nonz] * np.log(mm[reg][nonz]) - nc[reg][nonz] + nc[reg][nonz] * np.log(nc[reg][nonz]))
        isz = self.isz
        cstat = cstat + 2.0 * np.sum(mm[reg][isz])
        return cstat


class Fitter:

    def __init__(self, model, profile):
        self.mod = model
        self.profile = profile
        self.mlike = None
        self.params = None
        self.errors = None
        self.minuit = None
        self.out = None

    def Migrad(self, method='chi2', fitlow=None, fithigh=None, **kwargs):
        prof = self.profile
        if prof.profile is None:
            print('Error: No valid profile exists in provided object')
            return
        else:
            model = self.mod.model
            if prof.psfmat is not None:
                psfmat = np.transpose(prof.psfmat)
            else:
                psfmat = None
            if method == 'chi2':
                chi2 = ChiSquared(model, (prof.bins), (prof.profile), (prof.eprof), psfmat=psfmat, fitlow=fitlow, fithigh=fithigh)
                minuit = (iminuit.Minuit)(chi2, **kwargs)
            elif method == 'cstat':
                if prof.counts is None:
                    print('Error: No count profile exists')
                    return
                cstat = Cstat(model, (prof.bins), (prof.counts), (prof.area), (prof.effexp), (prof.bkgcounts), psfmat=psfmat, fitlow=fitlow, fithigh=fithigh)
                minuit = (iminuit.Minuit)(cstat, **kwargs)
            else:
                print('Unknown method ', method)
                return
        fmin, param = minuit.migrad()
        npar = len(minuit.values)
        outval = np.empty(npar)
        outerr = np.empty(npar)
        for i in range(npar):
            outval[i] = minuit.values[i]
            outerr[i] = minuit.errors[i]

        self.mod.SetParameters(outval)
        self.mod.SetErrors(outerr)
        self.mod.parnames = minuit.parameters
        self.params = minuit.values
        self.errors = minuit.errors
        self.mlike = fmin
        self.minuit = minuit
        self.out = param