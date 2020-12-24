# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/johnsalvatier/Documents/workspace/multichain_mcmc/multichain_mcmc/dream_examples/model2.py
# Compiled at: 2010-01-03 13:30:27
"""
Created on Nov 25, 2009

@author: johnsalvatier
"""
from numpy import *
import pymc
from scipy import stats
import pylab
ReData = arange(200, 3000, 25)
measured = 10.2 * ReData ** 0.5 + stats.distributions.norm(mu=0, scale=55).rvs(len(ReData))

def model_gen():
    varlist = []
    stdev = pymc.TruncatedNormal('stdev', mu=400, tau=1.0 / 160000, a=0, b=Inf)
    varlist.append(stdev)

    @pymc.deterministic
    def precision(stdev=stdev):
        return 1.0 / stdev ** 2

    a = pymc.TruncatedNormal('a', mu=1, tau=1.0 / 900, a=0, b=Inf)
    b = pymc.Uniform('b', lower=0.05, upper=2.0)
    varlist.append(a)
    varlist.append(b)

    @pymc.deterministic
    def nonlinear(Re=ReData, value=measured, a=a, b=b, observed=True):
        return a * ReData ** b

    results = pymc.Normal('results', mu=nonlinear, tau=precision, value=measured, observed=True)
    varlist.append(results)
    return varlist