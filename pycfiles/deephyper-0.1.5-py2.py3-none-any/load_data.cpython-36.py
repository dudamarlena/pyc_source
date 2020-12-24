# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/benchmark/nas/saddleReg/load_data.py
# Compiled at: 2019-06-18 16:53:11
# Size of source mod 2**32: 955 bytes
import os, numpy as np
from deephyper.benchmark.benchmark_functions_wrappers import saddle_
HERE = os.path.dirname(os.path.abspath(__file__))
np.random.seed(2018)

def load_data(dim=10):
    """
    Generate data for polynome_2 function.
    Returns Tuple of Numpy arrays: `(train_X, train_y), (valid_X, valid_y)`.
    """
    size = 100000
    prop = 0.8
    f, (a, b), _ = saddle_()
    d = b - a
    x = np.array([a + np.random.random(dim) * d for i in range(size)])
    y = np.array([[f(v)] for v in x])
    sep_index = int(prop * size)
    train_X = x[:sep_index]
    train_y = y[:sep_index]
    valid_X = x[sep_index:]
    valid_y = y[sep_index:]
    print(f"train_X shape: {np.shape(train_X)}")
    print(f"train_y shape: {np.shape(train_y)}")
    print(f"valid_X shape: {np.shape(valid_X)}")
    print(f"valid_y shape: {np.shape(valid_y)}")
    return ((train_X, train_y), (valid_X, valid_y))


if __name__ == '__main__':
    load_data()