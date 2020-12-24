# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/johnsalvatier/Documents/workspace/multichain_mcmc/multichain_mcmc/dream_examples/model4.py
# Compiled at: 2010-01-05 22:01:50
from numpy import *
import pymc
from scipy import stats
from scipy.stats import distributions as d
dimensions = 20
observations = 100
shape = (dimensions, observations)
trueFactorMagnitudes = d.norm(loc=0, scale=1).rvs(observations)
trueFactorLoadings = d.norm(loc=1, scale=0.2).rvs(dimensions)
trueErrorSds = d.gamma.rvs(5, scale=0.05, size=dimensions)
data = (trueFactorMagnitudes[newaxis, :] * trueFactorLoadings[:, newaxis] + d.norm(loc=0, scale=trueErrorSds[:, newaxis]).rvs(shape)).ravel()

def model_gen():
    variables = []
    factors = pymc.Normal('factormagnitudes', mu=zeros(observations), tau=ones(observations))
    limits = ones(dimensions) * -Inf
    limits[0] = 0.0
    loadings = pymc.TruncatedNormal('factorloadings', mu=ones(dimensions), tau=ones(dimensions) * 1.0, a=limits, b=Inf)
    returnSDs = pymc.Gamma('residualsds', alpha=ones(dimensions) * 1, beta=ones(dimensions) * 0.5)
    variables.append(loadings)
    variables.append(returnSDs)
    variables.append(factors)

    @pymc.deterministic
    def returnPrecisions(stdev=returnSDs):
        precisions = (ones(shape) * (stdev ** (-2))[:, newaxis]).ravel()
        return precisions

    @pymc.deterministic
    def meanReturns(factors=factors, loadings=loadings):
        means = factors[newaxis, :] * loadings[:, newaxis]
        return means.ravel()

    returns = pymc.Normal('returns', mu=meanReturns, tau=returnPrecisions, observed=True, value=data.ravel())
    variables.append(returns)
    return variables