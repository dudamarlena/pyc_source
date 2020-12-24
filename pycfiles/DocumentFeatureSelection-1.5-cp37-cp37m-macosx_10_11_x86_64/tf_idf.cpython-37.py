# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kensuke-mi/Desktop/analysis_work/document-feature-selection/DocumentFeatureSelection/tf_idf/tf_idf.py
# Compiled at: 2017-02-23 10:26:28
# Size of source mod 2**32: 1850 bytes
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from sklearn.feature_extraction.text import TfidfTransformer
from scipy.sparse.csr import csr_matrix
from numpy import ndarray
__author__ = 'kensuke-mi'

class TFIDF(object):

    def __init__(self, ngram=1, norm_metric='l2', use_idf_bool=True, smooth_idf_bool=True, sublinear_tf_bool=False):
        assert isinstance(ngram, int)
        self.n_gram = ngram
        self.norm_metric = norm_metric
        self.use_idf_bool = use_idf_bool
        self.smooth_idf_bool = smooth_idf_bool
        self.sublinear_tf_bool = sublinear_tf_bool

    def fit_transform(self, X):
        if isinstance(X, csr_matrix):
            X = X.toarray()
        else:
            X = X
        tf_idf_matrix = self.call_sklearn_tfidf(X=X,
          norm=(self.norm_metric),
          use_idf=(self.use_idf_bool),
          smooth_idf=(self.smooth_idf_bool),
          sublinear_tf=(self.sublinear_tf_bool))
        self.weighed_matrix = tf_idf_matrix
        return tf_idf_matrix

    def call_sklearn_tfidf(self, X, norm='l2', use_idf=True, smooth_idf=True, sublinear_tf=False):
        if not isinstance(X, (csr_matrix, ndarray)):
            raise AssertionError
        else:
            tf_idf_generator = TfidfTransformer(norm=norm,
              use_idf=use_idf,
              smooth_idf=smooth_idf,
              sublinear_tf=sublinear_tf)
            if isinstance(csr_matrix, csr_matrix):
                feat_matrix = X.toarray()
            else:
                feat_matrix = X
        tf_idf_weight_matrix = tf_idf_generator.fit_transform(X=feat_matrix)
        assert isinstance(tf_idf_weight_matrix, (csr_matrix, ndarray))
        return tf_idf_weight_matrix