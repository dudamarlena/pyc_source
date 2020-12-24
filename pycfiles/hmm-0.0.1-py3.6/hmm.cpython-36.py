# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hmm/hmm.py
# Compiled at: 2017-04-20 17:04:15
# Size of source mod 2**32: 1521 bytes
import numpy as np, scipy.stats as st
from scipy.misc import logsumexp

def gaussian_emission_forwards_backwards(signal, means, variances, transition_probs):
    """
    params:
    ------
    signal: an iterable of observed values
    means: an iterable of the means for each state
    variances: an iterable of the variances for each state
    transition_probs: a matrix where the value at row j column i is the
        probability of transitioning from state j to state i

    returns:
    ------
    gamma: a matrix where the value at row t column j is the probability of
        being in state j in timestep t
    """
    num_motifs = len(means)
    num_positions = len(signal)
    log_tp = np.log(transition_probs)
    probs = np.ones((num_positions, num_motifs))
    for t, s in enumerate(signal):
        probs[t] = st.norm.logpdf(s, means, variances)

    alpha = np.ones((num_positions, num_motifs))
    alpha[0] = probs[0] + log_tp[0]
    for t in range(1, num_positions):
        alpha[t] = probs[t] + logsumexp((log_tp.T + alpha[(t - 1)]), axis=1)

    beta = np.zeros((num_positions, num_motifs))
    for t in range(num_positions - 2, -1, -1):
        beta[t] = logsumexp((log_tp + (beta[(t + 1)] + probs[(t + 1)])), axis=1)

    gamma = alpha + beta
    for t in range(num_positions):
        gamma[t] = gamma[t] - logsumexp(gamma[t])

    return np.exp(gamma)