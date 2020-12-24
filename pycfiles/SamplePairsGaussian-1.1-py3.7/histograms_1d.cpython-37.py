# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/examples/histograms_1d.py
# Compiled at: 2019-06-29 21:36:16
# Size of source mod 2**32: 2804 bytes
from samplePairsGaussian import *
import sys, numpy as np
import matplotlib.pyplot as plt
if __name__ == '__main__':
    L = 100
    dim = 1
    N = 1000
    posns = (np.random.random(size=(N, dim)) - 0.5) * (2.0 * L)

    def handle_fail():
        print('Could not draw particle: try adjusting the std. dev. for the probability cutoff.')
        sys.exit(0)


    std_dev_tmp = 1.0
    prob_calculator = ProbCalculator(posns, dim, std_dev_tmp)
    sampler = Sampler(prob_calculator)

    def get_samples(no_samples, std_dev, std_dev_clip_mult):
        prob_calculator.set_std_dev(std_dev, std_dev_clip_mult)
        no_tries_max = 100
        idxs_1 = []
        idxs_2 = []
        for i in range(0, no_samples):
            success = sampler.rejection_sample(no_tries_max=no_tries_max)
            if not success:
                handle_fail()
            idxs_1.append(sampler.idx_first_particle)
            idxs_2.append(sampler.idx_second_particle)

        return [idxs_1, idxs_2]


    plt.figure()
    plt.hist(posns)
    plt.xlabel('particle position')
    plt.title('Distribution of ' + str(N) + ' particle positions')
    no_samples = 10000
    std_devs = [
     1.0, 10.0, 30.0]
    std_dev_clip_mult = 3.0
    for std_dev in std_devs:
        idxs_1, idxs_2 = get_samples(no_samples, std_dev, std_dev_clip_mult)
        plt.figure()
        idxs_1_symmetric = np.concatenate((idxs_1, idxs_2))
        idxs_2_symmetric = np.concatenate((idxs_2, idxs_1))
        plt.hist2d((posns[idxs_1_symmetric][:, 0]), (posns[idxs_2_symmetric][:, 0]), bins=(20,
                                                                                           20), cmap=(plt.cm.jet))
        plt.xlabel('position of particle #1')
        plt.ylabel('position of particle #2')
        plt.title('Std. dev. = ' + str(std_dev))

    plt.show()