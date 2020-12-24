# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: profile.py
# Compiled at: 2010-06-01 01:25:21
import model8, pymc, multichain_mcmc, numpy, cProfile

def sample():
    sampler = multichain_mcmc.AmalaSampler(model8.model_gen)
    sampler.sample(ndraw=500, maxGradient=1.3, mAccept=True, mConvergence=True)


cProfile.run('sample()', 'amala.profile')