# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/argument_esa_model/matrix.py
# Compiled at: 2020-05-12 09:02:27
# Size of source mod 2**32: 1135 bytes
import math, numpy as np
from scipy import sparse

class ESAMatrix:

    def __init__(self, terms, concepts, bows):
        self._terms = terms
        self._concepts = concepts
        self._mat = self._compute_tf_idf(bows)

    def _compute_tf_idf(self, bows):
        mat = sparse.lil_matrix((np.zeros((len(self._terms), len(self._concepts)))), dtype=(np.longdouble))
        for concept, bow in zip(self._concepts, bows):
            concept_length = sum(bow.values())
            for term in bow:
                mat[(self._terms.index(term), self._concepts.index(concept))] = bow[term] / concept_length

        mat = mat.tocsc()
        length = mat.get_shape()[1]
        for x in range(mat.get_shape()[0]):
            mat[x, :] *= math.log(length / mat[x, :].count_nonzero(), 10)

        mat.eliminate_zeros()
        return mat

    def get_mat(self):
        return self._mat

    def get_terms(self):
        return self._terms

    def get_concepts(self):
        return self._concepts

    def __getitem__(self, concept):
        return self._mat.getcol(self._concepts.index(concept))