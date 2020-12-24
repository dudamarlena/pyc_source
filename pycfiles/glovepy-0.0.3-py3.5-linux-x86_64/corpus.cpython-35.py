# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/glovepy/corpus.py
# Compiled at: 2017-08-18 13:54:44
# Size of source mod 2**32: 2899 bytes
import numpy as np
try:
    import cPickle as pickle
except ImportError:
    import pickle

from .corpus_cython import construct_cooccurrence_matrix

class Corpus(object):
    __doc__ = '\n    Class for constructing a cooccurrence matrix\n    from a corpus.\n\n    A dictionry mapping words to ids can optionally\n    be supplied. If left None, it will be constructed\n    from the corpus.\n    '

    def __init__(self, dictionary=None):
        self.dictionary = {}
        self.dictionary_supplied = False
        self.matrix = None
        if dictionary is not None:
            self._check_dict(dictionary)
            self.dictionary = dictionary
            self.dictionary_supplied = True

    def _check_dict(self, dictionary):
        if np.max(list(dictionary.values())) != len(dictionary) - 1:
            raise Exception('The largest id in the dictionary should be equal to its length minus one.')
        if np.min(list(dictionary.values())) != 0:
            raise Exception('Dictionary ids should start at zero')

    def fit(self, corpus, window=10, ignore_missing=False, symmetric=True):
        """
        Perform a pass through the corpus to construct
        the cooccurrence matrix.

        Parameters:
        - iterable of lists of strings corpus
        - int window: the length of the (symmetric)
          context window used for cooccurrence.
        - bool ignore_missing: whether to ignore words missing from
                               the dictionary (if it was supplied).
                               Context window distances will be preserved
                               even if out-of-vocabulary words are
                               ignored.
                               If False, a KeyError is raised.
        - bool symmetric: whether to get the context from both sides.
                          If False, only the left side context is considered.
        """
        self.matrix = construct_cooccurrence_matrix(corpus, self.dictionary, int(self.dictionary_supplied), int(window), int(ignore_missing), int(symmetric))

    def save(self, filename):
        with open(filename, 'wb') as (savefile):
            pickle.dump((self.dictionary, self.matrix), savefile, protocol=pickle.HIGHEST_PROTOCOL)

    @classmethod
    def load(cls, filename):
        instance = cls()
        with open(filename, 'rb') as (savefile):
            instance.dictionary, instance.matrix = pickle.load(savefile)
        return instance