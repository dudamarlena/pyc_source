# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/drqa/reader/data.py
# Compiled at: 2019-08-29 06:03:42
# Size of source mod 2**32: 4043 bytes
"""Data processing/loading helpers."""
import numpy as np, logging, unicodedata
from torch.utils.data import Dataset
from torch.utils.data.sampler import Sampler
from .vector import vectorize
logger = logging.getLogger(__name__)

class Dictionary(object):
    NULL = '<NULL>'
    UNK = '<UNK>'
    START = 2

    @staticmethod
    def normalize(token):
        return unicodedata.normalize('NFD', token)

    def __init__(self):
        self.tok2ind = {self.NULL: 0, self.UNK: 1}
        self.ind2tok = {0:self.NULL,  1:self.UNK}

    def __len__(self):
        return len(self.tok2ind)

    def __iter__(self):
        return iter(self.tok2ind)

    def __contains__(self, key):
        if type(key) == int:
            return key in self.ind2tok
        if type(key) == str:
            return self.normalize(key) in self.tok2ind

    def __getitem__(self, key):
        if type(key) == int:
            return self.ind2tok.get(key, self.UNK)
        if type(key) == str:
            return self.tok2ind.get(self.normalize(key), self.tok2ind.get(self.UNK))

    def __setitem__(self, key, item):
        if type(key) == int:
            if type(item) == str:
                self.ind2tok[key] = item
        elif type(key) == str:
            if type(item) == int:
                self.tok2ind[key] = item
        else:
            raise RuntimeError('Invalid (key, item) types.')

    def add(self, token):
        token = self.normalize(token)
        if token not in self.tok2ind:
            index = len(self.tok2ind)
            self.tok2ind[token] = index
            self.ind2tok[index] = token

    def tokens(self):
        """Get dictionary tokens.

        Return all the words indexed by this dictionary, except for special
        tokens.
        """
        tokens = [k for k in self.tok2ind.keys() if k not in frozenset({'<UNK>', '<NULL>'})]
        return tokens


class ReaderDataset(Dataset):

    def __init__(self, examples, model, single_answer=False):
        self.model = model
        self.examples = examples
        self.single_answer = single_answer

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, index):
        return vectorize(self.examples[index], self.model, self.single_answer)

    def lengths(self):
        return [(len(ex['document']), len(ex['question'])) for ex in self.examples]


class SortedBatchSampler(Sampler):

    def __init__(self, lengths, batch_size, shuffle=True):
        self.lengths = lengths
        self.batch_size = batch_size
        self.shuffle = shuffle

    def __iter__(self):
        lengths = np.array([(-l[0], -l[1], np.random.random()) for l in self.lengths],
          dtype=[
         (
          'l1', np.int_), ('l2', np.int_), ('rand', np.float_)])
        indices = np.argsort(lengths, order=('l1', 'l2', 'rand'))
        batches = [indices[i:i + self.batch_size] for i in range(0, len(indices), self.batch_size)]
        if self.shuffle:
            np.random.shuffle(batches)
        return iter([i for batch in batches for i in batch])

    def __len__(self):
        return len(self.lengths)