# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/examples/multiple_1d_multispecies.py
# Compiled at: 2019-06-29 21:38:30
# Size of source mod 2**32: 3028 bytes
from samplePairsGaussian import *
import sys, numpy as np
import matplotlib.pyplot as plt
if __name__ == '__main__':
    L = 100
    dim = 1
    N = 100
    posns = {}
    posns['A'] = (np.random.random(size=(N, dim)) - 0.5) * (2.0 * L)
    posns['B'] = (np.random.random(size=(N, dim)) - 0.5) * (2.0 * L)
    std_dev = 10.0
    std_dev_clip_mult = 3.0
    prob_calculator = ProbCalculatorMultiSpecies(posns, dim, std_dev, std_dev_clip_mult)
    sampler = SamplerMultiSpecies(prob_calculator)
    sampler.set_logging_level(logging.INFO)

    def handle_fail():
        print('Could not draw particle: try adjusting the std. dev. for the probability cutoff.')
        sys.exit(0)


    no_samples = 1000
    no_tries_max = 100
    idxs_1 = {'A':[],  'B':[]}
    idxs_2 = {'A':[],  'B':[]}
    for i in range(0, no_samples):
        success = sampler.rejection_sample(no_tries_max=no_tries_max)
        if not success:
            handle_fail()
        idxs_1[sampler.species_particles].append(sampler.idx_first_particle)
        idxs_2[sampler.species_particles].append(sampler.idx_second_particle)

    idxs_1['A'] = np.array(idxs_1['A']).astype(int)
    idxs_1['B'] = np.array(idxs_1['B']).astype(int)
    idxs_2['A'] = np.array(idxs_2['A']).astype(int)
    idxs_2['B'] = np.array(idxs_2['B']).astype(int)
    plt.figure()
    plt.hist(posns['A'])
    plt.xlabel('particle position')
    plt.title('Distribution of ' + str(N) + ' particle positions of species A')
    plt.figure()
    plt.hist(posns['B'])
    plt.xlabel('particle position')
    plt.title('Distribution of ' + str(N) + ' particle positions of species B')
    plt.figure()
    idxs_1_symmetric = np.concatenate((idxs_1['A'], idxs_2['A']))
    idxs_2_symmetric = np.concatenate((idxs_2['A'], idxs_1['A']))
    plt.plot(posns['A'][idxs_1_symmetric][:, 0], posns['A'][idxs_2_symmetric][:, 0], 'ro')
    idxs_1_symmetric = np.concatenate((idxs_1['B'], idxs_2['B']))
    idxs_2_symmetric = np.concatenate((idxs_2['B'], idxs_1['B']))
    plt.plot(posns['B'][idxs_1_symmetric][:, 0], posns['B'][idxs_2_symmetric][:, 0], 'bo')
    plt.xlabel('position of particle #1')
    plt.ylabel('position of particle #2')
    plt.title(str(no_samples) + ' sampled pairs of particles')
    plt.show()