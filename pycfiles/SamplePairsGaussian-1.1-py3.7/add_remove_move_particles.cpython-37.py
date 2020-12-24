# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/examples/add_remove_move_particles.py
# Compiled at: 2019-06-29 21:34:48
# Size of source mod 2**32: 3436 bytes
from samplePairsGaussian import *
import sys, numpy as np
if __name__ == '__main__':
    L = 5.0
    dim = 1
    N = 3
    posns = (np.random.random(size=(N, dim)) - 0.5) * (2.0 * L)
    std_dev = 3.0
    std_dev_clip_mult = None
    prob_calculator = ProbCalculator(posns=posns, dim=dim, std_dev=std_dev, std_dev_clip_mult=std_dev_clip_mult)
    print('--- Initial probabilities ---')
    for i_pair in range(0, prob_calculator.no_idx_pairs_possible):
        idx1 = prob_calculator.probs_idxs_first_particle[i_pair]
        idx2 = prob_calculator.probs_idxs_second_particle[i_pair]
        print('particles: ' + str(idx1) + ' @ ' + str(prob_calculator.posns[idx1]) + ' and ' + str(idx2) + ' @ ' + str(prob_calculator.posns[idx2]) + ' dist: ' + str(np.sqrt(prob_calculator.dists_squared[i_pair])) + ' prob: ' + str(prob_calculator.probs[i_pair]))

    idx_new = 1
    posn_new = np.array([0.5])
    prob_calculator.add_particle(idx_new, posn_new)
    print('--- After adding particle: idx: ' + str(idx_new) + ' posn: ' + str(posn_new) + ' ---')
    for i_pair in range(0, prob_calculator.no_idx_pairs_possible):
        idx1 = prob_calculator.probs_idxs_first_particle[i_pair]
        idx2 = prob_calculator.probs_idxs_second_particle[i_pair]
        print('particles: ' + str(idx1) + ' @ ' + str(prob_calculator.posns[idx1]) + ' and ' + str(idx2) + ' @ ' + str(prob_calculator.posns[idx2]) + ' dist: ' + str(np.sqrt(prob_calculator.dists_squared[i_pair])) + ' prob: ' + str(prob_calculator.probs[i_pair]))

    idx_remove = 2
    prob_calculator.remove_particle(idx_remove)
    print('--- After removing particle: idx: ' + str(idx_remove) + ' ---')
    for i_pair in range(0, prob_calculator.no_idx_pairs_possible):
        idx1 = prob_calculator.probs_idxs_first_particle[i_pair]
        idx2 = prob_calculator.probs_idxs_second_particle[i_pair]
        print('particles: ' + str(idx1) + ' @ ' + str(prob_calculator.posns[idx1]) + ' and ' + str(idx2) + ' @ ' + str(prob_calculator.posns[idx2]) + ' dist: ' + str(np.sqrt(prob_calculator.dists_squared[i_pair])) + ' prob: ' + str(prob_calculator.probs[i_pair]))

    idx_move = 1
    posn_move = np.array([0.6])
    prob_calculator.move_particle(idx_move, posn_move)
    print('--- After moving particle: idx: ' + str(idx_move) + ' from: ' + str(prob_calculator.posns[idx_move]) + ' to new pos: ' + str(posn_move) + ' ---')
    for i_pair in range(0, prob_calculator.no_idx_pairs_possible):
        idx1 = prob_calculator.probs_idxs_first_particle[i_pair]
        idx2 = prob_calculator.probs_idxs_second_particle[i_pair]
        print('particles: ' + str(idx1) + ' @ ' + str(prob_calculator.posns[idx1]) + ' and ' + str(idx2) + ' @ ' + str(prob_calculator.posns[idx2]) + ' dist: ' + str(np.sqrt(prob_calculator.dists_squared[i_pair])) + ' prob: ' + str(prob_calculator.probs[i_pair]))