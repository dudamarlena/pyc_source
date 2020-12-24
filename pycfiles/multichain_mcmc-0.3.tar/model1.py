# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/johnsalvatier/Documents/workspace/multichain_mcmc/multichain_mcmc/amala_examples/model1.py
# Compiled at: 2010-01-31 13:54:05
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

def model():
    varlist = []
    sd = pymc.Uniform('sd', lower=5, upper=100)
    varlist.append(sd)
    a = pymc.Uniform('a', lower=0, upper=100)
    b = pymc.Uniform('b', lower=0.05, upper=2.0)
    varlist.append(a)
    varlist.append(b)
    nonlinear = a * ReData ** b
    precision = sd ** (-2)
    results = pymc.Normal('results', mu=nonlinear, tau=precision, value=measured, observed=True)
    varlist.append(results)
    return varlist