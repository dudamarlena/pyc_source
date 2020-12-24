# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/johnsalvatier/Documents/workspace/multichain_mcmc/multichain_mcmc/dream_examples/model3.py
# Compiled at: 2010-01-06 01:15:47
"""
Created on Nov 25, 2009

@author: johnsalvatier
"""
from numpy import *
import pymc
from scipy import stats
import pylab
zeroStart = stats.distributions.norm(mu=0, scale=200).rvs(1)
ReData = arange(200, 5000, 10)
maxRe = max(ReData)
measured = 10.2 * ReData ** 0.5 + stats.distributions.norm(mu=0, scale=55).rvs(len(ReData)) + zeroStart
otherData = stats.distributions.norm(mu=zeroStart, scale=30).rvs(10)

def model_gen():
    varlist = []
    stdev = pymc.TruncatedNormal('stdev', mu=400, tau=1.0 / 160000, a=0, b=Inf)
    varlist.append(stdev)

    @pymc.deterministic
    def precision(stdev=stdev):
        return 1.0 / stdev ** 2

    fakeA = pymc.TruncatedNormal('a', mu=1, tau=1.0 / 2500, a=0, b=Inf)
    b = pymc.Uniform('b', lower=0.05, upper=2.0)
    a = fakeA * maxRe ** (-b)
    z = pymc.Normal('zero', mu=0, tau=1.0 / 160000)
    varlist.append(fakeA)
    varlist.append(a)
    varlist.append(b)
    varlist.append(z)

    @pymc.deterministic
    def nonlinear(Re=ReData, value=measured, a=a, b=b, z=z, observed=True):
        return a * ReData ** b + z

    results = pymc.Normal('results', mu=nonlinear, tau=precision, value=measured, observed=True)
    varlist.append(results)
    return varlist