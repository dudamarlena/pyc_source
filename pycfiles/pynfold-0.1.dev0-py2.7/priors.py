# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/pynfold/priors.py
# Compiled at: 2018-05-17 07:30:25
import pymc
priors = {}

def wrapper(priorname='', low=[], up=[], other_args={}, optimized=False):
    if priorname in priors:
        priormethod = priors[priorname]
    else:
        if hasattr(pymc, priorname):
            priormethod = getattr(pymc, priorname)
        else:
            print 'WARNING: prior name not found!'
            print 'Falling back to DiscreteUniform...'
            priormethod = pymc.DiscreteUniform
        truthprior = []
        for bin, (l, u) in enumerate(zip(low, up)):
            name = 'truth%d' % bin
            default_args = dict(name=name, value=l + (u - l) / 2, lower=l, upper=u)
            args = dict(default_args.items() + other_args.items())
            prior = priormethod(**args)
            truthprior.append(prior)

    return pymc.Container(truthprior)