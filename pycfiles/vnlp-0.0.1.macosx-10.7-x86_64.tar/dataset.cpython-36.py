# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/anaconda3/lib/python3.6/site-packages/vnlp/data/dataset.py
# Compiled at: 2018-06-21 22:40:12
# Size of source mod 2**32: 382 bytes
import numpy as np
from tqdm import tqdm

class Dataset(list):

    def batch(self, batch_size, shuffle=False, verbose=True):
        copy = self[:]
        if shuffle:
            np.random.shuffle(copy)
        iterator = range(0, len(copy), batch_size)
        iterator = tqdm(iterator) if verbose else iterator
        for i in iterator:
            yield copy[i:i + batch_size]