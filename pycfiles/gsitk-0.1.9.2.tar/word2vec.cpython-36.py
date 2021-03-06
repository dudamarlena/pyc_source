# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/oaraque/git/gsi/gsitk/gsitk/features/word2vec.py
# Compiled at: 2017-09-29 08:28:59
# Size of source mod 2**32: 2218 bytes
"""
Feature extraction with Word2Vec, as explained in

"Enhancing deep learning sentiment analysis with ensemble techniques in social
applications",
http://dx.doi.org/10.1016/j.eswa.2017.02.002

Needs a Word2Vec model previously trained.
Compatible with Gensim and Google word2vec format.
"""
import os, numpy as np
from gensim.models import Word2Vec
from gensim.models.keyedvectors import KeyedVectors
from gsitk.features.embeddings import Embedding
from sklearn.base import TransformerMixin

class Word2VecFeatures(Embedding, TransformerMixin):
    __doc__ = '\n    Implements the word2vec operations.\n    '

    def __init__(self, w2v_model_path, w2v_format='gensim', convolution=[
 1, 0, 0]):
        super(Word2VecFeatures, self).__init__(convolution)
        self.w2v_model_path = w2v_model_path
        self.w2v_format = w2v_format
        self.model = self.load_w2v()
        self.size = self._size()

    def _size(self):
        return self.model.vector_size

    def load_w2v(self):
        """Load Word2vec model with format awareness."""
        if not os.path.exists(self.w2v_model_path):
            raise ValueError('Word2Vec model path does not exist.')
        else:
            if self.w2v_format == 'gensim':
                w2v = Word2Vec.load(self.w2v_model_path)
            else:
                if self.w2v_format == 'google_txt':
                    w2v = KeyedVectors.load_word2vec_format((self.w2v_model_path), binary=False)
                else:
                    if self.w2v_format == 'google_bin':
                        w2v = KeyedVectors.load_word2vec_format((self.w2v_model_path), binary=True)
                    else:
                        raise ValueError('w2v_format={} is not valid.'.format(self.w2v_format))
        return w2v

    def transform(self, X):
        """Extract the features.
        This considers X to be a list of lists of texts.
        [
        ['my', 'dog', 'run', 'in', 'the', 'rain']
        ]

        w2v_format can be 'gensim', 'google_txt' or 'google_bin'
        """
        vecs = self.comments2vec(text=X)
        vecs = self.check_vector(vecs)
        return vecs

    def fit(self, x, y=None):
        return self