# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/data_reader/real_input.py
# Compiled at: 2018-07-20 17:29:00
# Size of source mod 2**32: 3232 bytes
from typing import List
from scipy.sparse import csr_matrix

class RealFeatureVector(object):
    __doc__ = 'Feature vector data structure.\n\n    Contains sparse representation of real_value features.\n    Defines basic methods for manipulation and data format changes.\n\n        '

    def __init__(self, num_features: int, feature_indices: List[int], data):
        """Create a feature vector given a set of known features.

        Args:
                num_features (int): Total number of features.
                feature_indices (List[int]): Indices of each feature present in instance.

                """
        self.indptr = [
         0, len(feature_indices)]
        self.feature_count = num_features
        self.indices = feature_indices
        self.data = data

    def copy(self, feature_vector):
        return RealFeatureVector(feature_vector.feature_count, feature_vector.indices, feature_vector.data)

    def __iter__(self):
        return iter(self.indices)

    def __getitem__(self, key):
        return self.indices[key]

    def __len__(self):
        return len(self.indices)

    def get_feature_count(self):
        """Return static number of features.

                """
        return self.feature_count

    def get_feature(self, index: int):
        """Return value of feature at index
                Args:
                        index (int): Feature index.
                """
        for i in range(len(self.indices)):
            if index == self.indices[i]:
                return self.data[i]

        return 0

    def flip_val(self, index, value):
        if index not in self.indices:
            if value == 0:
                return
            self.indices.append(index)
            self.indices.sort(reverse=True)
            self.indptr[1] += 1
            for i in range(len(self.indices)):
                if index == self.indices[i]:
                    self.data.insert(i, value)
                    return

        else:
            for i in range(len(self.indices)):
                if index == self.indices[i]:
                    if value != 0:
                        self.data[i] = value
                        return
                    self.indices.remove(index)
                    self.indptr[1] -= 1
                    self.data.pop(i)
                    return

    def get_csr_matrix(self) -> csr_matrix:
        """Return feature vector represented by sparse matrix.

                """
        data = self.data
        indices = self.indices
        indptr = [0, len(self.indices)]
        return csr_matrix((data, indices, indptr), shape=(
         1, self.feature_count))

    def feature_difference(self, xa):
        y_array = self.get_csr_matrix()
        xa_array = xa.get_csr_matrix()
        c_y = y_array - xa_array
        return c_y.data