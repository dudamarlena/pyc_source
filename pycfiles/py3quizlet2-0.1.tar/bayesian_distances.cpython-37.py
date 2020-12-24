# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/py3plex/algorithms/statistics/bayesian_distances.py
# Compiled at: 2019-02-25 14:07:54
# Size of source mod 2**32: 1003 bytes
import argparse
from .bayesiantests import *
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import numpy as np, seaborn as sns
from collections import defaultdict

def generate_bayesian_diagram(result_matrices, algo_names=[
 'algo1', 'algo2'], rope=0.01, rho=0.2, show_diagram=True, save_diagram=None):
    print(rope, rho)
    pl, pe, pr = hierarchical(result_matrices, rope, rho, verbose=True, names=algo_names)
    samples = hierarchical_MC(result_matrices, rope, rho, names=algo_names)
    fig = plot_posterior(samples, algo_names, proba_triplet=[np.round(pl, 2), pe, np.round(pr, 2)])
    if show_diagram:
        plt.show()
    if save_diagram is not None:
        plt.savefig(save_diagram)
    return (pl, pe, pr)