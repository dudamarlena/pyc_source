# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/pytransit/param/parameter.py
# Compiled at: 2020-01-13 18:32:58
# Size of source mod 2**32: 9001 bytes
import pandas as pd
from itertools import product
from numpy import inf, array, zeros, unique, where, stack, atleast_2d, squeeze, all
from .prior import DefaultPrior, NormalPrior, UniformPrior, JeffreysPrior, LogLogisticPrior, GammaPrior

class Parameter:

    def __init__(self, name, description='', unit='', prior=None, bounds=(-inf, inf), **kwargs):
        self.name = name
        self.description = description
        self.unit = unit
        self.prior = prior or DefaultPrior()
        self.bounds = bounds
        self.pid = -1
        self.scope = kwargs.get('scope', 'global')
        assert self.scope in ('global', 'local', 'passband')

    def __str__(self):
        return f"{self.pid:3d} |{self.scope[0].upper():1s}| {self.name:14s} {str(self.prior):40} [{self.bounds[0]:8.2f} .. {self.bounds[1]:8.2f}]"

    def __repr__(self):
        return str(self)

    def truncated_lnprior(self, v):
        if self.bounds[0] < v < self.bounds[1]:
            return self.prior.logpdf(v)
        return -inf

    def lnprior(self, v):
        return self.prior.logpdf(v)

    def rvs(self, size):
        return self.prior.rvs(size)


class GParameter(Parameter):

    def __init__(self, name, description='', unit='', prior=None, bounds=(-inf, inf), **kwargs):
        (super().__init__)(name, description, unit, prior, bounds, scope='global', **kwargs)


class LParameter(Parameter):

    def __init__(self, name, description='', unit='', prior=None, bounds=(-inf, inf), **kwargs):
        (super().__init__)(name, description, unit, prior, bounds, scope='local', **kwargs)


class PParameter(Parameter):

    def __init__(self, name, description='', unit='', prior=None, bounds=(-inf, inf), **kwargs):
        (super().__init__)(name, description, unit, prior, bounds, scope='passband', **kwargs)


class GParameterBlock:

    def __init__(self, name, start, stop):
        self.name = name
        self.start = start
        self.stop = stop
        self.slice = slice(self.start, self.stop)

    def __repr__(self):
        return "GParameterBlock('{}', {}, {})".format(self.name, self.start, self.stop)


class PParameterBlock(GParameterBlock):

    def __init__(self, name, start, stop, isize, npb):
        assert (stop - start) // isize == npb, 'The number of parameter sets != npb'
        assert (stop - start) % isize == 0
        super(PParameterBlock, self).__init__(name, start, stop)
        self.isize = isize
        self.nelem = nelem = (stop - start) // isize
        self.slice = slice(self.start, self.stop)
        self.slices = [slice(self.start + isize * i, self.start + isize * (i + 1)) for i in range(nelem)]

    def __repr__(self):
        return "<PParameterBlock('{}', {}, {}, {})".format(self.name, self.start, self.stop, self.isize)


class LParameterBlock(GParameterBlock):

    def __init__(self, name, start, stop, isize, nlc):
        assert (stop - start) // isize == nlc, 'The number of parameter sets != nlc '
        assert (stop - start) % isize == 0
        super(LParameterBlock, self).__init__(name, start, stop)
        self.isize = isize
        self.nelem = nelem = (stop - start) // isize
        self.slice = slice(self.start, self.stop)
        self.slices = [slice(self.start + isize * i, self.start + isize * (i + 1)) for i in range(nelem)]

    def __repr__(self):
        return "<LParameterBlock('{}', {}, {}, {})".format(self.name, self.start, self.stop, self.isize)


class ParameterSet(list):

    def __init__(self, *args):
        (super().__init__)(*args)
        self.blocks = []
        self.bounds = None
        self.frozen = False

    def add_global_block(self, name, pars):
        start = len(self)
        stop = start + len(pars)
        self.blocks.append(GParameterBlock(name, start, stop))
        self.extend(pars)

    def add_passband_block(self, name, isize, npb, pars):
        start = len(self)
        stop = start + len(pars)
        self.blocks.append(PParameterBlock(name, start, stop, isize, npb))
        self.extend(pars)

    def add_lightcurve_block(self, name, isize, nlc, pars):
        start = len(self)
        stop = start + len(pars)
        self.blocks.append(LParameterBlock(name, start, stop, isize, nlc))
        self.extend(pars)

    def append(self, *args):
        if not self.frozen:
            (super().append)(*args)
        else:
            raise ValueError('Trying to append to a frozen ParameterSet')

    def extend(self, *args):
        if not self.frozen:
            (super().extend)(*args)
        else:
            raise ValueError('Trying to extend a frozen ParameterSet')

    def _update_indices(self):
        if not self.frozen:
            self.bounds = array([p.bounds for p in self])
            self.lbounds = self.bounds[:, 0]
            self.ubounds = self.bounds[:, 1]
            for i, p in enumerate(self):
                p.pid = i

        else:
            raise ValueError('Trying to update a frozen ParameterSet')

    def lnprior(self, pv):
        pv = atleast_2d(pv)
        lnp = zeros(pv.shape[0])
        m = all(pv > self.bounds[:, 0], 1) & all(pv < self.bounds[:, 1], 1)
        for i, p in enumerate(self):
            lnp += p.lnprior(pv[:, i])

        return squeeze(where(m, lnp, -inf))

    def freeze(self):
        self._update_indices()
        self.frozen = True

    def thaw(self):
        self.frozen = False

    def validate(self):
        if not all(pd.Categorical(self.names).value_counts() == 1):
            raise ValueError('Duplicate parameter names are not allowed')
        else:
            pnames = self.passband_parameters.names
            if not all(['_' in name for name in pnames]):
                raise ValueError('Passband-dependent parameters must be named as parameter_passband')
            pars = unique(list((n.split('_')[0] for n in pnames)))
            pbs = unique(list((n.split('_')[1] for n in pnames)))
            if not len(self.passband_parameters) == len(pars) * len(pbs):
                raise ValueError('Passband-dependent parameters must exist for all passbands')
            assert all(['{}_{}'.format(pr, pb) in pnames for pr, pb in product(pars, pbs)]), 'Passband-dependent parameters must be named as parameter_passband'

    def find_pid(self, name):
        for p in self:
            if name == p.name:
                return p.pid

        raise KeyError('Could not find parameter {}'.format(name))

    def sample_from_prior(self, size=1):
        return stack([p.rvs(size) for p in self.priors], 1)

    def check_pv(self, pv):
        for i, p in enumerate(self):
            lnp = p.prior.logpdf(pv[i])
            b = self.bounds[i]
            is_finite = p.bounds[0] < pv[i] < p.bounds[1]
            print(f"|{p.pid:3d}| {'*' if not is_finite else ' '} {p.name:10} {b[0]:7.1f} < {pv[i]:10.2f} < {b[1]:<8.1f} {str(p.prior):40} log P = {lnp:6.2f}")

    @property
    def mean_pv(self):
        x0 = zeros(len(self))
        for i, p in enumerate(self.priors):
            if isinstance(p, NormalPrior):
                x0[i] = p.mean
            elif isinstance(p, UniformPrior):
                x0[i] = 0.5 * (p.a + p.b)
            else:
                raise ValueError

        return x0

    @property
    def names(self):
        return [p.name for p in self]

    @property
    def units(self):
        return [p.unit for p in self]

    @property
    def descriptions(self):
        return [p.description for p in self]

    @property
    def priors(self):
        return [p.prior for p in self]

    @property
    def scopes(self):
        return [p.scope for p in self]

    @property
    def global_parameters(self):
        return ParameterSet([p for p in self if p.scope == 'global'])

    @property
    def local_parameters(self):
        return ParameterSet([p for p in self if p.scope == 'local'])

    @property
    def passband_parameters(self):
        return ParameterSet([p for p in self if p.scope == 'passband'])