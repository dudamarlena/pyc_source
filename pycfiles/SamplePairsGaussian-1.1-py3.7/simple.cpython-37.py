# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/examples/simple.py
# Compiled at: 2019-06-29 21:24:23
# Size of source mod 2**32: 1453 bytes
from samplePairsGaussian import *
import sys, numpy as np
if __name__ == '__main__':
    L = 100
    dim = 1
    N = 100
    posns = (np.random.random(size=(N, dim)) - 0.5) * (2.0 * L)
    std_dev = 10.0
    std_dev_clip_mult = 3.0
    prob_calculator = ProbCalculator(posns, dim, std_dev, std_dev_clip_mult)
    sampler = Sampler(prob_calculator)
    sampler.set_logging_level(logging.INFO)

    def handle_fail():
        print('Could not draw particle: try adjusting the std. dev. for the probability cutoff.')
        sys.exit(0)


    no_tries_max = 100
    success = sampler.rejection_sample(no_tries_max=no_tries_max)
    if not success:
        handle_fail()
    success = sampler.cdf_sample()
    if not success:
        handle_fail()