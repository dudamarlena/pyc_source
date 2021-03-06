# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/bxa/xspec/priors.py
# Compiled at: 2020-01-28 12:31:59
# Size of source mod 2**32: 3189 bytes
__doc__ = '\nBXA (Bayesian X-ray Analysis) for Xspec\n\nCopyright: Johannes Buchner (C) 2013-2019\n\nPriors\n'
from __future__ import print_function
from math import log10

def create_uniform_prior_for(model, par):
    """
        Use for location variables (position)
        The uniform prior gives equal weight in non-logarithmic scale.
        """
    pval, pdelta, pmin, pbottom, ptop, pmax = par.values
    print('  uniform prior for %s between %f and %f ' % (par.name, pmin, pmax))
    low = float(pmin)
    spread = float(pmax - pmin)
    if pmin > 0:
        if pmax / pmin > 100:
            print('   note: this parameter spans several dex. Should it be log-uniform (create_jeffreys_prior_for)?')

    def uniform_transform(x):
        return x * spread + low

    return dict(model=model, index=(par._Parameter__index), name=(par.name), transform=uniform_transform,
      aftertransform=(lambda x: x))


def create_jeffreys_prior_for(model, par):
    """
        Use for scale variables (order of magnitude)
        The Jeffreys prior gives equal weight to each order of magnitude between the
        minimum and maximum value. Flat in logarithmic scale
        """
    pval, pdelta, pmin, pbottom, ptop, pmax = par.values
    print('  jeffreys prior for %s between %e and %e ' % (par.name, pmin, pmax))
    if pmin == 0:
        raise Exception('You forgot to set reasonable parameter limits on %s' % par.name)
    low = log10(pmin)
    spread = log10(pmax) - log10(pmin)
    if spread > 10:
        print('   note: this parameter spans *many* dex. Double-check the limits are reasonable.')

    def log_transform(x):
        return x * spread + low

    def log_after_transform(x):
        return 10 ** x

    return dict(model=model, index=(par._Parameter__index), name=('log(%s)' % par.name), transform=log_transform,
      aftertransform=log_after_transform)


def create_gaussian_prior_for(model, par, mean, std):
    """
        Use for informed variables.
        The Gaussian prior weights by a Gaussian in the parameter.
        """
    import scipy.stats
    pval, pdelta, pmin, pbottom, ptop, pmax = par.values
    rv = scipy.stats.norm(mean, std)

    def gauss_transform(x):
        return max(pmin, min(pmax, rv.ppf(x)))

    print('  gaussian prior for %s of %f +- %f' % (par.name, mean, std))
    return dict(model=model, index=(par._Parameter__index), name=(par.name), transform=gauss_transform,
      aftertransform=(lambda x: x))


def create_custom_prior_for(model, par, transform, aftertransform=lambda x: x):
    """
        Pass your own prior weighting transformation
        """
    print('  custom prior for %s' % par.name)
    return dict(model=model, index=(par._Parameter__index), name=(par.name), transform=transform,
      aftertransform=aftertransform)


def create_prior_function(transformations):
    """
        Creates a single prior transformation function from parameter transformations
        """

    def prior(cube, ndim, nparams):
        try:
            for i, t in enumerate(transformations):
                transform = t['transform']
                cube[i] = transform(cube[i])

        except Exception as e:
            print('ERROR: Exception in prior function. Faulty transformations specified!')
            print('ERROR:', e)
            print(i, transformations[i])
            import sys
            sys.exit(-126)

    return prior