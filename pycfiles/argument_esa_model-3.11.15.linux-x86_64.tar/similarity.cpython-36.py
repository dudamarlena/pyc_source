# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/argument_esa_model/similarity.py
# Compiled at: 2020-05-12 09:02:27
# Size of source mod 2**32: 1407 bytes
import numpy as np, time, sklearn.metrics.pairwise as sk
from scipy import sparse
from scipy.sparse.linalg import norm

class Similarity:

    def __init__(self):
        pass

    def cosine_similarity(input_vec, concept_mat):
        similarity = sk.cosine_similarity(input_vec.transpose().todense(), concept_mat)[0, :]
        return similarity

    def maximum_matching_similarity(model, input_vec, concept_vec, input_terms, corpus_terms):
        s = model.similarity
        comparisons = 0
        t1 = input_terms
        t2 = corpus_terms
        ind2 = concept_vec.indices
        similarity = 0.0
        for i in input_vec.indices:
            max_similarity = 0.0
            index = 0
            for j in ind2:
                comparisons += 1
                current_similarity = s(t1[i], t2[j])
                if current_similarity > max_similarity:
                    max_similarity = current_similarity
                    index = j
                if max_similarity >= 1.0:
                    break
                else:
                    continue

            similarity += (input_vec[i] * concept_vec[index])[(0, 0)] * max_similarity

        similarity /= norm(input_vec) * norm(concept_vec)
        return similarity

    def average_similarity(model, input_vec, concept_vec, input_terms, corpus_terms):
        raise NotImplementedError