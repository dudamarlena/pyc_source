# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/johnsalvatier/Documents/workspace/multichain_mcmc/multichain_mcmc/amala_examples/model8.py
# Compiled at: 2010-06-07 23:13:14
from numpy import *
import pymc
from scipy import stats
from scipy.stats import distributions as d
n = 100
x = random.normal(scale=0.2, size=n)

def model_gen():
    variables = []
    mu = pymc.Normal('mu', mu=0, tau=0.04)
    variables.append(mu)
    obs = pymc.Normal('obs', mu=mu, tau=24.999999999999996, observed=True, value=x)
    return variables