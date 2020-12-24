# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/oaraque/git/gsi/gsitk/gsitk/features/embeddings.py
# Compiled at: 2017-03-09 12:24:30
# Size of source mod 2**32: 1460 bytes
"""
Abstraction for embeddings methods, which wraps the common functionalities
used when performing embeddings operations.
"""
import numpy as np
from gsitk.features.features import Features

class Embedding(Features):
    __doc__ = '\n    Abstraction for the embeddings operations.\n    '

    def __init__(self, conv=[1, 0, 0]):
        self.conv = conv

    def build_vec(self, text):
        vecs = np.zeros((len(text), self.size))
        for i, word in enumerate(text):
            try:
                vecs[i] = self.model[word]
            except KeyError:
                continue

        if self.conv[0]:
            return np.average(vecs, axis=0)
        if self.conv[1]:
            return np.amax(vecs, axis=0)
        if self.conv[2]:
            return np.amin(vecs, axis=0)

    def comments2vec(self, text):
        """
        Convert to vecs the text passed as a iterator.
        The conv parameter defines the convolutional function to use:
        [x,x,x] <=> [average, max, min]
        Only one convolutional function by pass is supported.
        We consider each one a different type of feature.
        """
        l = len(text)
        vecs = np.zeros((l, self.size))
        for i in range(l):
            vecs[i] = self.build_vec(text=(text[i]))

        return vecs

    def check_vector(self, v):
        if np.any(np.isnan(v)):
            v_ = np.zeros((v.shape[0],))
        else:
            v_ = v
        return v_