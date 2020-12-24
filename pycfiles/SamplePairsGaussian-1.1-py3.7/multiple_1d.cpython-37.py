# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/examples/multiple_1d.py
# Compiled at: 2019-06-29 21:39:50
# Size of source mod 2**32: 2296 bytes
from samplePairsGaussian import *
import sys, numpy as np
import matplotlib.pyplot as plt
if __name__ == '__main__':
    L = 100
    dim = 1
    N = 100
    posns = (np.random.random(size=(N, dim)) - 0.5) * (2.0 * L)
    std_dev = 10.0
    std_dev_clip_mult = 3.0
    prob_calculator = ProbCalculator(posns, dim, std_dev, std_dev_clip_mult)
    sampler = Sampler(prob_calculator)

    def handle_fail():
        print('Could not draw particle: try adjusting the std. dev. for the probability cutoff.')
        sys.exit(0)


    no_samples = 1000
    no_tries_max = 100
    idxs_1 = []
    idxs_2 = []
    for i in range(0, no_samples):
        success = sampler.rejection_sample(no_tries_max=no_tries_max)
        if not success:
            handle_fail()
        idxs_1.append(sampler.idx_first_particle)
        idxs_2.append(sampler.idx_second_particle)

    idxs_1 = np.array(idxs_1).astype(int)
    idxs_2 = np.array(idxs_2).astype(int)
    plt.figure()
    plt.hist(posns)
    plt.xlabel('particle position')
    plt.title('Distribution of ' + str(N) + ' particle positions')
    plt.figure()
    idxs_1_symmetric = np.concatenate((idxs_1, idxs_2))
    idxs_2_symmetric = np.concatenate((idxs_2, idxs_1))
    plt.plot(posns[idxs_1_symmetric][:, 0], posns[idxs_2_symmetric][:, 0], 'o')
    plt.xlabel('position of particle #1')
    plt.ylabel('position of particle #2')
    plt.title(str(no_samples) + ' sampled pairs of particles')
    plt.show()