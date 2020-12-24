# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python2.7/site-packages/amltlearn/preprocessing/Discretizer.py
# Compiled at: 2015-09-02 05:29:36
__doc__ = '\n.. module:: Discretizer\n\nDiscretizer\n*************\n\n:Description: Discretizer\n\n    \n\n:Authors: bejar\n    \n\n:Version: \n\n:Created on: 13/03/2015 16:15 \n\n'
__author__ = 'bejar'
import numpy as np
from sklearn.base import TransformerMixin

class Discretizer(TransformerMixin):
    """
    Discretization of the attributes of a dataset (unsupervised)

    Parameters:

    method: str
     * 'equal' equal sized bins
     * 'frequency' bins with the same number of examples
    bins: int
     number of bins
    """
    intervals = None

    def __init__(self, method='equal', bins=2):
        self.method = method
        self.bins = bins

    def _fit(self, X):
        """
        Computes the discretization intervals

        :param matrix X:
        :return:
        """
        if self.method == 'equal':
            self._fit_equal(X)
        elif self.method == 'frequency':
            self._fit_frequency(X)

    def _fit_equal(self, X):
        """
        Computes the discretization intervals for equal sized discretization

        :param X:
        :return:
        """
        self.intervals = np.zeros((self.bins, X.shape[1]))
        for i in range(X.shape[1]):
            vmin = np.min(X[:, i])
            vmax = np.max(X[:, i])
            step = np.abs(vmax - vmin) / float(self.bins)
            for j in range(self.bins):
                vmin += step
                self.intervals[(j, i)] = vmin

            self.intervals[(self.bins - 1, i)] += 1e-11

    def _fit_frequency(self, X):
        """
        Computes the discretization intervals for equal frequency

        :param X:
        :return:
        """
        self.intervals = np.zeros((self.bins, X.shape[1]))
        quant = X.shape[0] / float(self.bins)
        for i in range(X.shape[1]):
            lvals = sorted(X[:, i])
            nb = 0
            while nb < self.bins:
                self.intervals[(nb, i)] = lvals[(int(quant * nb + quant) - 1)]
                nb += 1

            self.intervals[(self.bins - 1, i)] += 1e-11

    def _transform(self, X, copy=False):
        """
        Discretizes the attributes of a dataset

        :param matrix X: Data matrix
        :return:
        """
        if self.intervals is None:
            raise Exception('Discretizer: Not fitted')
        if copy:
            y = X.copy()
        else:
            y = X
        self.__transform(y)
        return y

    def __discretizer(self, v, at):
        """
        Determines the dicretized value for an atribute
        :param v:
        :return:
        """
        i = 0
        while i < self.intervals.shape[0] and v > self.intervals[(i, at)]:
            i += 1

        return i

    def __transform(self, X):
        """
        Applies the discretization to all the attributes of the data matrix

        :param X:
        :return:
        """
        for i in range(X.shape[1]):
            for j in range(X.shape[0]):
                X[(j, i)] = self.__discretizer(X[(j, i)], i)

    def fit(self, X):
        """
        Fits a set of discretization intervals using the data in X

        :param matrix X: The data matrix
        """
        self._fit(X)

    def transform(self, X, copy=False):
        """
        Applies previously fitted discretization intervals to X

        :param matrix X: The data matrix
        :param bool copy: Returns a copy of the transformed datamatrix
        :return: The transformed datamatrix
        """
        return self._transform(X, copy=copy)

    def fit_transform(self, X, copy=False):
        """
        Fits and transforms the data

        :param matrix X: The data matrix
        :param bool copy: Returns a copy of the transformed datamatrix
        :return:The transformed datamatrix
        """
        self._fit(X)
        return self._transform(X, copy=copy)