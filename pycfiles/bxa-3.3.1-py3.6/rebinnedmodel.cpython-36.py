# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bxa/sherpa/rebinnedmodel.py
# Compiled at: 2020-01-28 12:31:59
# Size of source mod 2**32: 5835 bytes
from __future__ import print_function
from sherpa.astro.ui import *
from sherpa.models.parameter import Parameter
from sherpa.models import ArithmeticModel
import itertools, numpy
from tqdm import tqdm
from monointerp import interp

class RebinnedModel(ArithmeticModel):

    def __init__(self, slowmodel, ebins, parameters, filename, modelname='rebinnedmodel'):
        params = [param for param, nbins in parameters]
        bins = [numpy.linspace(param.min, param.max, nbins) for param, nbins in parameters]
        left = ebins[:-1]
        right = ebins[1:]
        width = right - left
        ntot = numpy.product([len(bin) for bin in bins])
        try:
            alldata = numpy.load(filename)
            data = alldata['y']
            assert numpy.allclose(alldata['x'], ebins), 'energy binning differs -- plese delete "%s"' % filename
            print('loaded from %s' % filename)
        except IOError:
            print('creating rebinnedmodel, this might take a while')
            print('interpolation setup:')
            print('   energies:', ebins[0], ebins[1], '...', ebins[(-2)], ebins[(-1)])
            for (param, nbins), bin in zip(parameters, bins):
                print('   %s: %s - %s with %d points' % (param.fullname, param.min, param.max, nbins))
                print('        ', bin)

            data = numpy.zeros((ntot, len(ebins) - 1))
            for j, element in enumerate(tqdm((itertools.product)(*bins), disable=None)):
                for i, p in enumerate(params):
                    if p.val != element[i]:
                        p.val = element[i]

                values = [p.val for p in slowmodel.pars]
                model = slowmodel.calc(values, left, right)
                data[j] = model

            print('model created. storing to %s' % filename)
            numpy.savez(filename, x=ebins, y=data)

        self.init(modelname=modelname, x=ebins, data=data, parameters=parameters)

    def init(self, modelname, x, data, parameters):
        self.data = data
        pars = []
        for param, nbins in parameters:
            lo = param.min
            hi = param.max
            newp = Parameter(modelname=modelname, name=(param.name), val=(param.val),
              min=lo,
              max=hi,
              hard_min=lo,
              hard_max=hi)
            setattr(self, param.name, newp)
            pars.append(newp)

        newp = Parameter(modelname=modelname, name='norm', val=1, min=0, max=10000000000.0, hard_min=(-1e+300), hard_max=1e+300)
        self.norm = newp
        pars.append(newp)
        newp = Parameter(modelname=modelname, name='redshift', val=0, min=0, max=10, hard_min=0, hard_max=100)
        self.redshift = newp
        pars.append(newp)
        self.x = x
        self.binnings = [(param.min, param.max, nbins) for param, nbins in parameters]
        super(RebinnedModel, self).__init__(modelname, pars=pars)

    def get(self, coords):
        j = 0
        for i, ((lo, hi, n), c) in list(enumerate(zip(self.binnings, coords))):
            k = int((c - lo) * n / (hi - lo))
            if k == n:
                k = n - 1
            j = j * n + k

        return self.data[j]

    def calc(self, p, left, right, *args, **kwargs):
        coords = p[:-2]
        norm = p[(-2)]
        redshift = p[(-1)]
        shiftedleft = left * (1.0 + redshift)
        shiftedright = right * (1.0 + redshift)
        x = self.x
        y = self.get(coords)
        left = x[:-1]
        right = x[1:]
        width = right - left
        if not (y >= 0).all():
            raise AssertionError
        else:
            yw = y.cumsum()
            r = interp(shiftedleft, shiftedright, x, yw)
            assert numpy.isfinite(r).all(), r
        return r * norm