# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/johnsalvatier/Documents/workspace/multichain_mcmc/multichain_mcmc/dream_examples/model6.py
# Compiled at: 2010-01-05 21:42:25
from numpy import *
import pymc
from scipy import stats
from scipy.stats import distributions as d
dimensions = 100
observations = 100
shape = (dimensions, observations)
data = d.norm(loc=0, scale=1).rvs((dimensions, observations))

def model_gen():
    variables = []
    means = pymc.Normal('means', mu=zeros(dimensions), tau=ones(dimensions))
    sds = pymc.Gamma('sds', alpha=ones(dimensions) * 1, beta=ones(dimensions) * 1)
    variables.append(means)
    variables.append(sds)

    @pymc.deterministic
    def precisions(stdev=sds):
        precisions = (ones(shape) * (stdev ** (-2))[:, newaxis]).ravel()
        return precisions

    @pymc.deterministic
    def obsMeans(means=means):
        return (ones(shape) * means[:, newaxis]).ravel()

    obs = pymc.Normal('obs', mu=obsMeans, tau=precisions, observed=True, value=data.ravel())
    variables.append(obs)
    return variables