# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-n5kV9S/pyflux/pyflux/inference/norm_post_sim.py
# Compiled at: 2018-02-01 11:59:15
import numpy as np
from math import exp
import sys
if sys.version_info < (3, ):
    range = xrange
from scipy.stats import multivariate_normal

def norm_post_sim(modes, cov_matrix):
    post = multivariate_normal(modes, cov_matrix)
    nsims = 30000
    phi = np.zeros([nsims, len(modes)])
    for i in range(0, nsims):
        phi[i] = post.rvs()

    chain = np.array([ phi[i][0] for i in range(len(phi)) ])
    for m in range(1, len(modes)):
        chain = np.vstack((chain, [ phi[i][m] for i in range(len(phi)) ]))

    mean_est = [ np.mean(np.array([ phi[i][j] for i in range(len(phi)) ])) for j in range(len(modes)) ]
    median_est = [ np.median(np.array([ phi[i][j] for i in range(len(phi)) ])) for j in range(len(modes)) ]
    upper_95_est = [ np.percentile(np.array([ phi[i][j] for i in range(len(phi)) ]), 95) for j in range(len(modes)) ]
    lower_95_est = [ np.percentile(np.array([ phi[i][j] for i in range(len(phi)) ]), 5) for j in range(len(modes)) ]
    return (
     chain, mean_est, median_est, upper_95_est, lower_95_est)