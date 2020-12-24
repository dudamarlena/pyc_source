# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/feldbauer/PycharmProjects/hubness/skhubness/data/load_dataset.py
# Compiled at: 2019-08-29 04:04:59
# Size of source mod 2**32: 972 bytes
import os, numpy as np
__all__ = [
 'load_dexter']

def load_dexter() -> (
 np.ndarray, np.ndarray):
    """Load the example data set (dexter).

    Returns
    -------
    X, y : ndarray, ndarray
        Vector data, and class labels
    """
    n = 300
    dim = 20000
    dexter_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'dexter')
    dexter_labels = os.path.join(dexter_path, 'dexter_train.labels')
    dexter_vectors = os.path.join(dexter_path, 'dexter_train.data')
    y = np.loadtxt(dexter_labels)
    X = np.zeros((n, dim))
    with open(dexter_vectors, mode='r') as (fid):
        data = fid.readlines()
    row = 0
    for line in data:
        line = line.strip().split()
        for word in line:
            col, val = word.split(':')
            X[row][int(col) - 1] = int(val)

        row += 1

    return (X, y)