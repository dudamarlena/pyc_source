# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/local/Library/Frameworks/Python.framework/Versions/3.4/lib/python3.4/site-packages/vbmfa/fa.py
# Compiled at: 2014-10-04 10:11:28
# Size of source mod 2**32: 16128 bytes
"""Variational Bayesian Factor Analyser.

Implementation of a single factor analyser.
Model parameters are inferred by variational Bayes.
"""
import numpy as np
from scipy.special import digamma

class VbFa(object):
    __doc__ = 'Variational Bayesian Factor Analyser\n\n    Takes a :math:`p \\times n` data matrix :math:`y` with :math:`n` samples\n    :math:`y_i` of dimension :math:`p`, and describes them as a linear\n    combination of :math:`q` latent factors:\n\n    .. math::\n\n        P(y_i|\\Lambda, x_i, \\Psi) = N(y_i|\\Lambda x_i + \\mu, \\Psi)\n\n    :math:`\\Lambda` is the :math:`p \\times q` factor matrix, :math:`x_i` the\n    :math:`q` dimensional representation of :math:`y_i`, :math:`\\mu` the mean\n    vector, and :math:`\\Psi` the diagonal noise matrix.\n\n    Parameters\n    ----------\n    y : :py:class:`numpy.ndarray`\n        Data matrix with samples in columns and features in rows\n    q : int\n        Dimension of low-dimensional space (# factors)\n    hyper : :py:class:`fa.Hyper`\n\n    Attributes\n    ----------\n    Y : :py:class:`numpy.ndarray`\n        Data matrix with samples in columns and features in rows\n    P : int\n        Dimension of high-dimensional space\n    Q : int\n        Dimension of low-dimensional space (# factors)\n    N : int\n        # Samples\n    hyper : :py:class:`fa.Hyper`\n        Hyperparameters\n    q_nu : :py:class:`fa.Nu`\n        Nu distribution\n    q_mu : :py:class:`fa.Mu`\n        Mu distribution\n    q_lambda : :py:class:`fa.Lambda`\n        Lambda distribution\n    q_x : :py:class:`fa.X`\n        X distribution\n\n    Examples\n    --------\n    .. code:: python\n\n        fa = VbFa(data, q=2)\n        fa.fit()\n        print(fa.q_lambda.mean)\n        print(fa.q_x.mean)\n    '

    def __init__(self, y, q=None, hyper=None):
        self.Y = y
        self.P = self.Y.shape[0]
        self.Q = self.P if q is None else q
        self.N = self.Y.shape[1]
        if hyper is None:
            self.HYPER = Hyper(self.P, self.Q)
        else:
            self.HYPER = hyper
        self.q_nu = Nu(self.Q)
        self.q_mu = Mu(self.P)
        self.q_lambda = Lambda(self.P, self.Q)
        self.q_x = X(self.Q, self.N)

    def fit(self, maxit=10, eps=0.0, verbose=False):
        """Fit model parameters by updating factors for several iterations
        and return number of update iterations.

        Parameters
        ----------
        maxit : int
            Maximum number of update iterations
        eps : float
            Stop if change in MSE is below eps
        verbose : bool
            Print statistics

        Returns
        -------
        num_it : int
            Number of iterations
        """
        self.init()
        i = 0
        while i < maxit:
            mse_old = self.mse()
            self.update()
            mse_new = self.mse()
            delta = mse_old - mse_new
            i += 1
            if verbose:
                print('{:d}: {:.3f}'.format(i, mse_new))
            if delta < eps:
                break

        return i

    def mse(self):
        """Compute mean squared error (MSE) between original data and
        reconstructed data.

        Returns
        -------
        mse : float
            Mean squared error

        """
        return np.linalg.norm(self.Y - self.x_to_y())
        self.q_x = X(self.Q, self.N)

    def x_to_y(self, x=None):
        """Reconstruct data from low-dimensional representation.

        Parameters
        ----------
        x : :py:class:`numpy.ndarray`
            low-dimensional representation of the data

        Returns
        -------
        y : :py:class:`numpy.ndarray`
            High-dimensional representation
        """
        if x is None:
            x = self.q_x.mean
        return self.q_lambda.mean.dot(x) + self.q_mu.mean[:, np.newaxis]

    def q(self, name):
        """Return distribution q with the given name.

        Parameters
        ----------
        name : str
            Name of the q distribution
        """
        if name == 'nu':
            return self.q_nu
        if name == 'lambda':
            return self.q_lambda
        if name == 'x':
            return self.q_x
        if name == 'mu':
            return self.q_mu
        raise 'q_{:s} unknown!'.format(name)

    def init(self):
        """Initialize factors for fitting."""
        self.q_mu.mean = self.Y.mean(1)

    def update_nu(self):
        """Update nu distribution."""
        self.q_nu.update(self.HYPER, self.q_lambda)

    def update_lambda(self, x_s=None):
        """Update lambda distribution.

        Parameters
        ----------
        x_s : :py:class:`numpy.ndarray`
            sample weights
        """
        self.q_lambda.update(self.HYPER, self.q_mu, self.q_nu, self.q_x, self.Y, x_s=x_s)

    def update_x(self):
        """Update x distribution."""
        self.q_x.update(self.HYPER, self.q_lambda, self.q_mu, self.Y)

    def update_mu(self, x_s=None):
        """Update mu distribution.

        Parameters
        ----------
        x_s : :py:class:`numpy.ndarray`
            sample weights
        """
        self.q_mu.update(self.HYPER, self.q_lambda, self.q_x, self.Y, x_s=x_s)

    def update(self, names=[
 'lambda', 'x', 'nu', 'mu'], **kwargs):
        """Update all distributions once in the given order.

        Parameters
        ----------
        names : list
            Names of distribution to be updated
        """
        if type(names) is str:
            if names == 'nu':
                self.update_nu()
            else:
                if names == 'lambda':
                    self.update_lambda(**kwargs)
                else:
                    if names == 'mu':
                        self.update_mu(**kwargs)
                    elif names == 'x':
                        self.update_x()
        else:
            for name in names:
                self.update(name, **kwargs)

    def variance_explained(self, sort=False, norm=True):
        """Compute variance explained by factors.

        Parameters
        ----------
        sort : bool
            Sort variance explained in descending order
        norm : bool
            Normalize variance explained to sum up to one

        Returns
        -------
        variance_explained : float
            Variance explained
        """
        ve = np.array([l.dot(l) for l in self.q_lambda.mean.T])
        if sort:
            ve = np.sort(ve)[::-1]
        if norm:
            ve /= ve.sum()
        return ve

    def factors_order(self):
        """Return order of factors by their fraction of variance explained."""
        ve = self.variance_explained()
        return ve.argsort()[::-1]

    def permute(self, order):
        """Permute factors in the given order.

        Parameters
        ----------
        order : :py:class:`numpy.ndarray`
            Permutation order
        """
        self.q_lambda.permute(order)
        self.q_nu.permute(order)
        self.q_x.permute(order)

    def order_factors(self):
        """Orders factors by the fraction of variance explained."""
        self.permute(self.factors_order())


class Hyper(object):
    __doc__ = 'Class for model hyperparameters.\n\n    Parameters\n    ----------\n    p : int\n        Dimension of the high-dimensional space\n    q : int\n        Dimension of the low-dimensional space\n\n    Attributes\n    ----------\n    P : int\n        Dimension of the high-dimensional space\n    Q : int\n        Dimension of the low-dimensional space\n    a : float\n        Alpha parameter of gamma prior over factor matrix\n    b : float\n        Beta parameter of gamma prior over factor matrix\n    mu : :py:class:`numpy.ndarray`\n        P dimensional mean vector of normal prior over mu vector\n    nu : :py:class:`numpy.ndarray`\n        P dimensional precision vector of diagonal mu covariance matrix\n    psi : :py:class:`numpy.ndarray`\n        P dimensional precision vector of diagonal noise covariance matrix\n    '

    def __init__(self, p, q=None):
        self.P = p
        self.Q = p if q is None else q
        self.a = 1.0
        self.b = 1.0
        self.mu = np.zeros(self.P)
        self.nu = np.ones(self.P)
        self.psi = np.ones(self.P) * 10.0

    def __str__(self):
        s = '\na: {:f}, b: {:f}'.format(self.a, self.b)
        s += '\nmu: {:s}'.format(self.mu.__str__())
        s += '\nnu: {:s}'.format(self.nu.__str__())
        s += '\npsi: {:s}'.format(self.psi.__str__())
        return s


class Nu(object):
    __doc__ = 'Nu factor class.\n\n    Dirichlet distribution over factor matrix.\n\n    Parameters\n    ----------\n    q : int\n        Rank (# columns) of factor matrix\n\n    Attributes\n    ----------\n    Q : int\n        Rank (# columns) of factor matrix\n    a : float\n        Alpha parameter of Dirichlet distribution\n    b : float\n        Beta parameter of Dirichlet distribution\n    '

    def __init__(self, q):
        self.Q = q
        self.init()

    def init(self):
        """Initialize parameters."""
        self.a = 1.0
        self.b = np.ones(self.Q)

    def update(self, hyper, q_lambda):
        """Update parameter.

        Parameters
        ----------
        hyper : :py:class:`fa.Hyper`
            Hyperparameters
        q_lambda : :py:class:`fa.Lambda`
            Factor matrix
        """
        self.a = hyper.a + 0.5 * hyper.P
        self.b.fill(hyper.b)
        self.b += 0.5 * (np.sum(q_lambda.mean ** 2, 0) + np.diag(np.sum(q_lambda.cov, 0)))
        assert np.all(self.b > hyper.b)

    def __str__(self):
        return 'a: {:f}\nb: {:s}'.format(self.a, self.b.__str__())

    def expectation(self):
        """Return expectation of Dirichlet distribution."""
        return self.a / self.b

    def permute(self, order):
        """Permute factors in the given order.

        Parameters
        ----------
        order : :py:class:`numpy.ndarray`
            Permutation order
        """
        self.b = self.b[order]


class Mu(object):
    __doc__ = 'Mu factor class.\n\n    Normal distribution over mu with diagonal covariance matrix.\n\n    Parameters\n    ----------\n    p : int\n        dimension of mu vector\n\n    Attributes\n    ----------\n    P : int\n        dimension of mu vector\n    mean : :py:class:`np.ndarray`\n        mean of Normal distribution\n    cov : :py:class:`np.ndarray`\n        diagonal of covariance matrix\n    '

    def __init__(self, p):
        self.P = p
        self.init()

    def init(self):
        """Initialize parameters."""
        self.mean = np.random.normal(loc=0.0, scale=0.001, size=self.P)
        self.cov = np.ones(self.P)

    def __str__(self):
        return 'mean:\n{:s}\ncov:\n{:s}'.format(self.mean.__str__(), self.cov.__str__())

    def update(self, hyper, q_lambda, q_x, y, x_s=None):
        """Update parameters.

        Parameters
        ----------
        hyper : :py:class:`fa.Hyper`
            Hyperparameters
        q_lambda : :py:class:`fa.Lambda`
            Factor matrix
        q_x : :py:class:`fa.X`
            Factor loadings matrix
        x_s : :py:class:`numpy.ndarray`
            Sample weights
        """
        if x_s is None:
            x_s = np.ones(q_x.N)
        self.cov = hyper.nu + hyper.psi * np.sum(x_s)
        self.cov = self.cov ** (-1)
        self.mean = np.multiply(hyper.psi, (y - q_lambda.mean.dot(q_x.mean)).dot(x_s)) + np.multiply(hyper.mu, hyper.nu)
        self.mean = np.multiply(self.cov, self.mean)


class Lambda(object):
    __doc__ = 'Lambda factor matrix class.\n\n    Normal distributions over P rows of lambda matrix.\n\n    Parameters\n    ----------\n    p : int\n        # Rows of lambda matrix\n    q : int\n        # Columns of lambda matrix\n\n    Attributes\n    ----------\n    P : int\n        # Rows of lambda matrix\n    Q : int\n        # Columns of lambda matrix\n    mean : :py:class:`numpy.ndarray`\n        Mean of lambda matrix\n    cov : :py:class:`numpy.ndarray`\n        P QxQ covariance matrices for all rows\n    '

    def __init__(self, p, q):
        self.P = p
        self.Q = q
        self.init()

    def init(self):
        """Initialize parameters."""
        self.mean = np.random.normal(loc=0.0, scale=1.0, size=self.P * self.Q).reshape(self.P, self.Q)
        self.cov = np.empty((self.P, self.Q, self.Q))
        for p in range(self.P):
            self.cov[p] = np.eye(self.Q)

    def __str__(self, cov=False):
        s = 'mean:\n{:s}'.format(self.mean.__str__())
        if cov:
            for p in range(self.P):
                s += '\ncov[{:d}]:\n{:s}'.format(p, self.cov[p].__str__())

        return s

    def update(self, hyper, q_mu, q_nu, q_x, y, x_s=None):
        """Update parameters.

        Parameters
        ----------
        hyper : :py:class:`fa.Hyper`
            Hyperparameters
        q_mu : :py:class:`fa.Mu`
            Mu distribution
        q_nu : :py:class:`fa.Nu`
            Nu distribution
        q_x : :py:class:`fa.X`
            X distribution
        y : :py:class:`numpy.ndarray`
            Data matrix
        x_s : :py:class:`numpy.ndarray`
            Sample weights
        """
        if x_s is None:
            x_s = np.ones(q_x.N)
        assert np.all(q_nu.b > 0.0)
        t = np.zeros((self.Q, self.Q))
        for n in range(len(x_s)):
            t += x_s[n] * (np.outer(q_x.mean[:, n], q_x.mean[:, n]) + q_x.cov)

        tt = np.diag(q_nu.expectation())
        self.cov = np.empty((self.P, self.Q, self.Q))
        for p in range(self.P):
            self.cov[p] = tt + hyper.psi[p] * t
            self.cov[p] = np.linalg.inv(self.cov[p])

        self.mean = np.empty((self.P, self.Q))
        for p in range(self.P):
            w = np.multiply(x_s, y[p] - q_mu.mean[p])
            self.mean[p] = hyper.psi[p] * self.cov[p].dot(q_x.mean.dot(w))

    def permute(self, order):
        """Permute factors in the given order.

        Parameters
        ----------
        order : :py:class:`numpy.ndarray`
            Permutation order
        """
        self.mean = self.mean[:, order]
        for p in range(self.P):
            self.cov[p] = self.cov[p, order, :]
            self.cov[p] = self.cov[p, :, order]


class X(object):
    __doc__ = 'X factor class.\n\n    Normal distributions over N columns of X matrix.\n\n    Parameters\n    ----------\n    q : int\n        # Rows of X matrix\n    n : int\n        # Columns (# samples) of X matrix\n\n    Attributes\n    ----------\n    Q : int\n        # Rows of X matrix\n    N : int\n        # Columns (# samples) of X matrix\n    mean : :py:class:`numpy.ndarray`\n        QxN mean of X matrix\n    cov : :py:class:`numpy.ndarray`\n        QxQ covariance matrix shared for all N columns (samples)\n    '

    def __init__(self, q, n):
        self.Q = q
        self.N = n
        self.init()

    def init(self):
        """Initialize parameters."""
        self.mean = np.random.normal(loc=0.0, scale=1.0, size=self.Q * self.N).reshape(self.Q, self.N)
        self.cov = np.eye(self.Q)

    def update(self, hyper, q_lambda, q_mu, y):
        """Update parameters.

        Parameters
        ----------
        hyper : :py:class:`fa.Hyper`
            Hyperparameters
        q_lambda : :py:class:`fa.Lambda`
            Lambda distribution
        q_mu : :py:class:`fa.Mu`
            Mu distribution
        y : :py:class:`numpy.ndarray`
            Data matrix
        """
        self.cov = np.eye(self.Q) + np.multiply(q_lambda.mean.transpose(), hyper.psi).dot(q_lambda.mean)
        for p in range(len(hyper.psi)):
            self.cov += hyper.psi[p] * q_lambda.cov[p]

        self.cov = np.linalg.inv(self.cov)
        self.mean = self.cov.dot(np.multiply(q_lambda.mean.transpose(), hyper.psi).dot(y - q_mu.mean[:, np.newaxis]))

    def __str__(self):
        return 'mean:\n{:s}\ncov:\n{:s}'.format(self.mean.transpose().__str__(), self.cov.__str__())

    def permute(self, order):
        """ Permute factors in the given order.

        Parameters
        ----------
        order : :py:class:`numpy.ndarray`
            Permutation order
        """
        self.mean = self.mean[order, :]
        self.cov = self.cov[order, :]
        self.cov = self.cov[:, order]