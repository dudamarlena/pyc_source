# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pygp/util/pca.py
# Compiled at: 2013-04-10 06:45:39
"""
Created on 10 Sep 2012

@author: maxz
"""
import numpy, pylab

class PCA(object):
    """
    PCA module with automatic primal/dual usage.
    """

    def __init__(self, X):
        self.mu = X.mean(0)
        self.sigma = X.std(0)
        X = self.center(X)
        if X.shape[0] >= X.shape[1]:
            self.eigvals, self.eigvectors = self._primal_eig(X)
        else:
            self.eigvals, self.eigvectors = self._dual_eig(X)
        self.sort = numpy.argsort(self.eigvals)[::-1]
        self.eigvals = self.eigvals[self.sort]
        self.eigvectors = self.eigvectors[:, self.sort]
        self.fracs = self.eigvals / self.eigvals.sum()
        self.Q = self.eigvals.shape[0]

    def center(self, X):
        X = X - self.mu
        X = X / self.sigma
        return X

    def _primal_eig(self, X):
        return numpy.linalg.eigh(numpy.cov(X.T))

    def _dual_eig(self, X):
        dual_eigvals, dual_eigvects = numpy.linalg.eigh(numpy.cov(X))
        relevant_dimensions = numpy.argsort(numpy.abs(dual_eigvals))[-X.shape[1]:]
        eigvals = dual_eigvals[relevant_dimensions]
        eigvects = dual_eigvects[:, relevant_dimensions]
        eigvects = 1.0 / numpy.sqrt(X.shape[0] * numpy.abs(eigvals)) * X.T.dot(eigvects)
        eigvects /= numpy.sqrt(numpy.diag(eigvects.T.dot(eigvects)))
        return (eigvals, eigvects)

    def project(self, X, Q=None):
        """
        Project X into PCA space, defined by the Q highest eigenvalues.
        
        Y = X dot V
        """
        if Q is None:
            Q = self.Q
        if Q > X.shape[1]:
            raise IndexError('requested dimension larger then input dimension')
        X = self.center(X)
        return X.dot(self.eigvectors[:, :Q])

    def plot_fracs(self, Q=None, ax=pylab.gca()):
        if Q is None:
            Q = self.Q
        ticks = numpy.arange(Q)
        ax.bar(ticks - 0.4, self.fracs[:Q])
        ax.set_xticks(ticks, map(lambda x: ('${}$').format(x), ticks + 1))
        ax.set_ylabel('Eigenvalue fraction')
        ax.set_xlabel('PC')
        ax.set_ylim(0, ax.get_ylim()[1])
        ax.set_xlim(ticks.min() - 0.5, ticks.max() + 0.5)
        try:
            pylab.tight_layout()
        except:
            pass

        return

    def plot_2d(self, X, labels=None, s=20, c='b', marker='+', ax=pylab.gca(), ulabels=None, **kwargs):
        if labels is None:
            labels = numpy.zeros(X.shape[0])
        if ulabels is None:
            ulabels = numpy.unique(labels)
        nlabels = len(ulabels)
        if len(c) != nlabels:
            from matplotlib.cm import jet
            c = [ jet(float(i) / nlabels) for i in range(nlabels) ]
        X = self.project(X, 2)
        kwargs.update(dict(s=s))
        plots = list()
        for i, l in enumerate(ulabels):
            kwargs.update(dict(color=c[i], marker=marker[(i % len(marker))]))
            plots.append(ax.scatter(label=str(l), *X[labels == l, :].T, **kwargs))

        ax.set_xlabel('PC$_1$')
        ax.set_ylabel('PC$_2$')
        try:
            pylab.tight_layout()
        except:
            pass

        return plots