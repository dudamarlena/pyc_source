# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/py3plex/algorithms/statistics/correlation_networks.py
# Compiled at: 2019-02-24 13:10:35
# Size of source mod 2**32: 1805 bytes
import numpy as np
from collections import Counter
from scipy import stats

def pick_threshold(matrix):
    current_r_opt = 0
    rho, pval = stats.spearmanr(matrix)
    for j in np.linspace(0, 1, 50):
        tmp_array = rho.copy()
        tmp_array[tmp_array > j] = 1
        tmp_array[tmp_array < j] = 0
        np.fill_diagonal(tmp_array, 0)
        rw_sum = np.sum(tmp_array, axis=0)
        counts = Counter(rw_sum)
        key_counts = np.log(list(counts.keys()))
        counts = np.log(list(counts.values()))
        slope, intercept, r_value, p_value, std_err = stats.linregress(key_counts, counts)
        if r_value > current_r_opt:
            print('Updating R^2: {}'.format(r_value))
            current_r_opt = r_value
        if r_value > 0.8:
            return j

    return current_r_opt


def default_correlation_to_network(matrix, input_type='matrix', preprocess='standard'):
    if preprocess == 'standard':
        matrix = (matrix - np.mean(matrix, axis=0)) / np.std(matrix, axis=0)
    optimal_threshold = pick_threshold(matrix)
    print('Rsq threshold {}'.format(optimal_threshold))
    matrix[matrix > optimal_threshold] = 1
    matrix[matrix < optimal_threshold] = 0
    return matrix


if __name__ == '__main__':
    from numpy import genfromtxt
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', default='/home/skblaz/Downloads/expression.tsv')
    args = parser.parse_args()
    datta = args.filename
    a = genfromtxt(datta, delimiter='\t', skip_header=4)
    a = np.nan_to_num(a)
    print('Read the data..')
    print(default_correlation_to_network(a).shape)