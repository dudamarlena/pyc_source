# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python2.7/site-packages/amltlearn/feature_selection/unsupervised/LaplacianScore.py
# Compiled at: 2015-09-02 08:06:18
__doc__ = '\n.. module:: LaplacianScore\n\nLaplacianScore\n*************\n\n:Description: LaplacianScore\n\n    Class that computes the laplacian score for a dataset\n\n:Authors: bejar\n    \n\n:Version: \n\n:Created on: 25/11/2014 9:32 \n\n'
__author__ = 'bejar'
import numpy as np
from sklearn.neighbors import kneighbors_graph, NearestNeighbors
from operator import itemgetter

class LaplacianScore:
    """
    Laplacian Score algorithm

    Parameters:

       n_neighbors: int
        Number of neighbors to compute the similarity matrix
       bandwidth: float
        Bandwidth for the gaussian similarity kernel
    """
    scores_ = None

    def __init__(self, n_neighbors=5, bandwidth=0.01, k=None):
        """
        Initial values of the parameters

        :param int n_neighbors: Number of neighbors for the spectral matrix
        :param float bandwidth: Bandwidth for the gaussian kernel
        :param int k: number of features to select
        """
        self._n_neighbors = n_neighbors
        self._bandwidth = bandwidth
        self._k = k

    def fit(self, X):
        """
        Computes the laplacian scores for the dataset

        :param matrix X: is a [n_examples, n_attributes] numpy array
        """
        self._fit_process(X)
        return self

    def _best_k_scores(self, k=5):
        """
        returns the indices of the best k attributes according to the score

        :param k:
        :return:
        """
        if self.scores_ is None:
            raise Exception('Laplacian Score: Not fitted')
        else:
            l = list(enumerate(self.scores_))
            l = sorted(l, key=itemgetter(1), reverse=True)
            return [ l[i][0] for i in range(k) ]
        return

    def fit_transform(self, X):
        """
        Selects the features and returns the dataset with only the k best ones

        :param matrix X: dataset
        :return:
        """
        self._fit_process(X)
        l = list(enumerate(self.scores_))
        l = sorted(l, key=itemgetter(1), reverse=True)
        lsel = [ l[i][0] for i in range(self._k) ]
        return X[:, lsel]

    def _fit_process(self, X):
        """
        Computes the Laplacian score for the attributes

        :param X:
        :return:
        """
        self.scores_ = np.zeros(X.shape[1])
        S = kneighbors_graph(X, n_neighbors=self._n_neighbors, mode='distance')
        S = S.toarray()
        S *= S
        S /= self._bandwidth
        S = -S
        ones = np.ones(X.shape[0])
        D = np.diag(np.dot(S, ones))
        L = D - S
        qt = D.sum()
        for at in range(X.shape[1]):
            Fr = X[:, at]
            Fr_hat = Fr - np.dot(np.dot(Fr, D) / qt, ones)
            score1 = np.dot(np.dot(Fr_hat, L), Fr_hat)
            score2 = np.dot(np.dot(Fr_hat, D), Fr_hat)
            self.scores_[at] = score1 / score2