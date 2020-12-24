# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/library_simulator/util.py
# Compiled at: 2019-06-03 11:51:45
# Size of source mod 2**32: 2456 bytes
__description__ = '\nUtilities for analyzing output of simulated libraries.\n'
__author__ = 'Michael J. Harms'
__date__ = '2019-05-31'
from matplotlib import pyplot as plt
import numpy as np, pandas as pd

def freq_vs_mutation_rate(lib, mutation_rates=None, num_samples=10000, collapse_above=7):
    """
    Extract the frequency of different mutation classes from a library across
    a collection of mutation rates.

    lib: initialized instance of LibrarySimulator
    mutation_rates: list-like of floats containing mutation rates to use for
                    the calculation.  If none, rates between 0 and 20.
    num_samples: int. How big to make each library for the frequency calculation.
    collapse_above: put every mutation with more than this many mutations 
                    into its own bin.
    """
    if mutation_rates is None:
        mutation_rates = np.linspace(0, 20, 40)
    outs = []
    for i in range(collapse_above + 1):
        outs.append([])

    outs.append([])
    dead = []
    for rate in mutation_rates:
        lib.simulate(num_samples=num_samples, mutation_rate=rate)
        bad = lib.clones.indel | lib.clones.stop | lib.clones.start
        good = np.logical_not(bad)
        for i in range(collapse_above + 1):
            outs[i].append(sum(lib.clones.num[good] == i))

        outs[(i + 1)].append(sum(lib.clones.num[good] >= i + 1))
        dead.append(sum(bad))

    out = pd.DataFrame({'mut_rate': mutation_rates})
    for i in range(collapse_above):
        out['{}'.format(i)] = np.array(outs[i]) / num_samples

    out['{}+'.format(i + 1)] = np.array(outs[(i + 1)]) / num_samples
    out['dead'] = np.array(dead) / num_samples
    return out


def plot_freq_vs_mutation_rate(f_v_r):
    """
    Plot the frequency of each class of mutations against the mutation rate.
    """
    f_v_r.columns
    for m in f_v_r.columns[1:]:
        plt.plot(f_v_r['mut_rate'], f_v_r[m])

    plt.xlabel('mutation rate')
    plt.ylabel('frequency')
    plt.legend()