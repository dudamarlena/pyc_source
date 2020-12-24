# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/federatedml/feature/sparse_vector.py
# Compiled at: 2020-04-28 09:16:53
# Size of source mod 2**32: 1924 bytes


class SparseVector(object):
    __doc__ = '\n    Sparse storage data format of federatedml\n\n    Parameters\n    ----------\n    sparse_vec : dict, record (indice, data) kv tuples\n\n    shape : the real feature shape of data\n\n    '

    def __init__(self, indices=None, data=None, shape=0):
        self.sparse_vec = dict(zip(indices, data))
        self.shape = shape

    def get_data(self, pos, default_val=None):
        return self.sparse_vec.get(pos, default_val)

    def count_non_zeros(self):
        return len(self.sparse_vec)

    def count_zeros(self):
        return self.shape - len(self.sparse_vec)

    def get_shape(self):
        return self.shape

    def get_all_data(self):
        for idx, data in self.sparse_vec.items():
            yield (idx, data)

    def get_sparse_vector(self):
        return self.sparse_vec

    def set_sparse_vector(self, sparse_vec):
        self.sparse_vec = sparse_vec