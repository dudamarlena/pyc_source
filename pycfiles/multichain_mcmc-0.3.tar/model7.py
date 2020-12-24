# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/johnsalvatier/Documents/workspace/multichain_mcmc/multichain_mcmc/amala_examples/model7.py
# Compiled at: 2010-02-24 13:55:58
from numpy import *
import pymc
from scipy import stats
from scipy.stats import distributions as d
nPredictors = 60
observations = 400
trueIntercept = d.norm(loc=0, scale=20).rvs(1)
trueResponses = d.norm(loc=0, scale=2).rvs(nPredictors)
trueErrorSd = d.gamma.rvs(3, scale=0.5, size=1)
print 'true sd', trueErrorSd
observedPredictors = d.norm(loc=0, scale=1.0).rvs((nPredictors, observations))
data = trueIntercept + sum(observedPredictors * trueResponses[:, newaxis], axis=0) + d.norm(loc=0, scale=trueErrorSd).rvs(observations)

def model_gen():
    variables = []
    intercept = pymc.Normal('intercept', mu=0, tau=0.0004)
    sd = pymc.Gamma('sd', alpha=3, beta=2.0)
    responses = pymc.Normal('responses', mu=zeros((nPredictors, 1)), tau=ones((nPredictors, 1)) * 0.04)
    variables.append(intercept)
    variables.append(responses)
    variables.append(sd)
    obsMeans = intercept + pymc.sum(responses * observedPredictors, axis=0)
    obs = pymc.Normal('obs', mu=obsMeans, tau=sd ** (-2), observed=True, value=data)
    variables.append(obs)
    return variables