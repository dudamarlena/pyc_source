# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/examples/sample_2d.py
# Compiled at: 2019-06-29 21:42:03
# Size of source mod 2**32: 2957 bytes
from samplePairsGaussian import *
import sys, numpy as np
import matplotlib.pyplot as plt
if __name__ == '__main__':
    dim = 2
    N = 1000
    posns = np.random.normal(0.0, 10.0, size=(N, dim))
    std_dev = 1.0
    std_dev_clip_mult = 3.0
    prob_calculator = ProbCalculator(posns, dim, std_dev, std_dev_clip_mult)
    sampler = Sampler(prob_calculator)

    def handle_fail(ith_particle):
        print('Could not draw the ' + str(ith_particle) + ' particle: try adjusting the std. dev. for the probability cutoff.')
        sys.exit(0)


    no_samples = 10000
    no_tries_max = 100
    idxs_1 = []
    idxs_2 = []
    for i in range(0, no_samples):
        success = sampler.rejection_sample(no_tries_max=no_tries_max)
        if not success:
            handle_fail(i)
        idxs_1.append(sampler.idx_first_particle)
        idxs_2.append(sampler.idx_second_particle)

    dists = {}
    for i in range(0, no_samples):
        idx1 = idxs_1[i]
        idx2 = idxs_2[i]
        pos1 = posns[idx1]
        pos2 = posns[idx2]
        dist = np.sqrt(sum(pow(pos1 - pos2, 2)))
        if idx1 in dists:
            dists[idx1].append(dist)
        else:
            dists[idx1] = [
             dist]
        if idx2 in dists:
            dists[idx2].append(dist)
        else:
            dists[idx2] = [
             dist]

    ave_dist = np.full(N, 0.0)
    for idx, dist in dists.items():
        ave_dist[idx] = np.mean(dist)

    counts = np.full(N, 0).astype(int)
    for idx, dist in dists.items():
        counts[idx] = len(dist)

    plt.figure()
    min_dist = min(ave_dist)
    max_dist = max(ave_dist - min_dist)
    cols = [(dist - min_dist) / max_dist for dist in ave_dist]
    plt.scatter((posns[:, 0]), (posns[:, 1]), c=cols, cmap=(plt.cm.jet))
    plt.colorbar()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(str(N) + ' particles: ave dist of other particle')
    plt.figure()
    min_count = min(counts)
    max_count = max(counts - min_count)
    cols = [(count - min_count) / max_count for count in counts]
    plt.scatter((posns[:, 0]), (posns[:, 1]), c=cols, cmap=(plt.cm.jet))
    plt.colorbar()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(str(N) + ' particles: counts of draws')
    plt.show()