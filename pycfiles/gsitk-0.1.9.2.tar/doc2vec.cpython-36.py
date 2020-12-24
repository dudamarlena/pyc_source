# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/oaraque/git/gsi/gsitk/gsitk/features/doc2vec.py
# Compiled at: 2017-10-30 10:30:47
# Size of source mod 2**32: 1457 bytes
"""
Feature extraction with Doc2Vec, as explained in

"Enhancing deep learning sentiment analysis with ensemble techniques in social
applications",
http://dx.doi.org/10.1016/j.eswa.2017.02.002

Needs a Doc2Vec model previously trained.
Compatible with Gensim.
"""
import os, numpy as np
from gensim.models import Doc2Vec
from gsitk.features.embeddings import Embedding
from sklearn.base import TransformerMixin

class Doc2VecFeatures(Embedding, TransformerMixin):
    __doc__ = '\n    Implements Doc2Vec operations.\n    '

    def __init__(self, d2v_model_path):
        self.d2v_model_path = d2v_model_path
        self.model = self.load_d2v()
        self.size = self._size()

    def _size(self):
        return self.model.vector_size

    def load_d2v(self):
        """Load Word2vec model with format awareness."""
        if not os.path.exists(self.d2v_model_path):
            raise ValueError('Doc2Vec model path does not exist.')
        d2v = Doc2Vec.load(self.d2v_model_path)
        return d2v

    def build_vec(self, text):
        vec = self.model.infer_vector(text)
        return vec

    def transform(self, X):
        """Extract the features.
        This considers X to be a list of lists of texts.
        [
        ['my', 'dog', 'run', 'in', 'the', 'rain']
        ]"""
        vecs = self.comments2vec(text=X)
        vecs = self.check_vector(vecs)
        return vecs

    def fit(self, x, y=None):
        return self