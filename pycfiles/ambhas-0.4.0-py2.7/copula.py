# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ambhas/copula.py
# Compiled at: 2012-11-13 09:04:09
"""
Created on Wed Feb  9 19:13:28 2011

@ author:                  Sat Kumar Tomer 
@ author's webpage:        http://civil.iisc.ernet.in/~satkumar/
@ author's email id:       satkumartomer@gmail.com
@ author's website:        www.ambhas.com

"""
from __future__ import division
from scipy.stats import kendalltau, pearsonr, spearmanr
import numpy as np
from scipy.integrate import quad
from scipy.optimize import fmin
import sys, statistics as st
from scipy.interpolate import interp1d
from stats import scoreatpercentile

class Copula:
    """
    This class estimate parameter of copula
    generate joint random variable for the parameters
    This class has following three copulas:
        Clayton
        Frank
        Gumbel
        
    Example:
        x = np.random.normal(size=100)
        y = np.random.normal(size=100)
        foo = Copula(x, y, 'frank')
        u,v = foo.generate(100)
    """

    def __init__(self, X, Y, family):
        """ initialise the class with X and Y
        Input:
            X:        one dimensional numpy array
            Y:        one dimensional numpy array
            family:   clayton or frank or gumbel
            
            Note: the size of X and Y should be same
        """
        if not (X.ndim == 1 and Y.ndim == 1):
            raise ValueError('The dimension of array should be one.')
        if X.size != Y.size:
            raise ValueError('The size of both array should be same.')
        copula_family = [
         'clayton', 'frank', 'gumbel']
        if family not in copula_family:
            raise ValueError('The family should be clayton or frank or gumbel')
        self.X = X
        self.Y = Y
        self.family = family
        tau = kendalltau(self.X, self.Y)[0]
        self.tau = tau
        self.pr = pearsonr(self.X, self.Y)[0]
        self.sr = spearmanr(self.X, self.Y)[0]
        self._get_parameter()
        self.U = None
        self.V = None
        return

    def _get_parameter(self):
        """ estimate the parameter (theta) of copula
        """
        if self.family == 'clayton':
            self.theta = 2 * self.tau / (1 - self.tau)
        elif self.family == 'frank':
            self.theta = -fmin(self._frank_fun, -5, disp=False)[0]
        elif self.family == 'gumbel':
            self.theta = 1 / (1 - self.tau)

    def generate_uv(self, n=1000):
        """
        Generate random variables (u,v)
        
        Input:
            n:        number of random copula to be generated
        
        Output:
            U and V:  generated copula
            
        """
        if self.family == 'clayton':
            U = np.random.uniform(size=n)
            W = np.random.uniform(size=n)
            if self.theta <= -1:
                raise ValueError('the parameter for clayton copula should be more than -1')
            elif self.theta == 0:
                raise ValueError('The parameter for clayton copula should not be 0')
            if self.theta < sys.float_info.epsilon:
                V = W
            else:
                V = U * (W ** (-self.theta / (1 + self.theta)) - 1 + U ** self.theta) ** (-1 / self.theta)
        elif self.family == 'frank':
            U = np.random.uniform(size=n)
            W = np.random.uniform(size=n)
            if self.theta == 0:
                raise ValueError('The parameter for frank copula should not be 0')
            if abs(self.theta) > np.log(sys.float_info.max):
                V = (U < 0) + np.sign(self.theta) * U
            elif abs(self.theta) > np.sqrt(sys.float_info.epsilon):
                V = -np.log((np.exp(-self.theta * U) * (1 - W) / W + np.exp(-self.theta)) / (1 + np.exp(-self.theta * U) * (1 - W) / W)) / self.theta
            else:
                V = W
        elif self.family == 'gumbel':
            if self.theta <= 1:
                raise ValueError('the parameter for GUMBEL copula should be greater than 1')
            if self.theta < 1 + sys.float_info.epsilon:
                U = np.random.uniform(size=n)
                V = np.random.uniform(size=n)
            else:
                u = np.random.uniform(size=n)
                w = np.random.uniform(size=n)
                w1 = np.random.uniform(size=n)
                w2 = np.random.uniform(size=n)
                u = (u - 0.5) * np.pi
                u2 = u + np.pi / 2
                e = -np.log(w)
                t = np.cos(u - u2 / self.theta) / e
                gamma = (np.sin(u2 / self.theta) / t) ** (1 / self.theta) * t / np.cos(u)
                s1 = (-np.log(w1)) ** (1 / self.theta) / gamma
                s2 = (-np.log(w2)) ** (1 / self.theta) / gamma
                U = np.array(np.exp(-s1))
                V = np.array(np.exp(-s2))
        self.U = U
        self.V = V
        return (U, V)

    def generate_xy(self, n=1000):
        """
        Generate random variables (x, y)
        
        Input:
            n:        number of random copula to be generated
        
        Output:
            X1 and Y1:  generated copula random numbers
            
        """
        if self.U is None:
            self.generate_uv(n)
        self._inverse_cdf()
        X1 = self._inv_cdf_x(self.U)
        Y1 = self._inv_cdf_y(self.V)
        self.X1 = X1
        self.Y1 = Y1
        return (
         X1, Y1)

    def estimate(self, data=None):
        """
        this function estimates the mean, std, iqr for the generated
        ensemble

        Output:
            Y1_mean = mean of the simulated ensemble
            Y1_std = std of the simulated ensemble
            Y1_ll = lower limit of the simulated ensemble
            Y1_ul = upper limit of the simulated ensemble
        """
        nbin = 50
        try:
            self.X1
            copula_ens = len(self.X1)
        except:
            copula_ens = 10000
            self.generate_xy(copula_ens)

        if data is None:
            data = self.X
        n_ens = copula_ens / nbin
        ind_sort = self.X1.argsort()
        x_mean = np.zeros((nbin,))
        y_mean = np.zeros((nbin,))
        y_ul = np.zeros((nbin,))
        y_ll = np.zeros((nbin,))
        y_std = np.zeros((nbin,))
        for ii in range(nbin):
            x_mean[ii] = self.X1[ind_sort[n_ens * ii:n_ens * (ii + 1)]].mean()
            y_mean[ii] = self.Y1[ind_sort[n_ens * ii:n_ens * (ii + 1)]].mean()
            y_std[ii] = self.Y1[ind_sort[n_ens * ii:n_ens * (ii + 1)]].std()
            y_ll[ii] = scoreatpercentile(self.Y1[ind_sort[n_ens * ii:n_ens * (ii + 1)]], 25)
            y_ul[ii] = scoreatpercentile(self.Y1[ind_sort[n_ens * ii:n_ens * (ii + 1)]], 75)

        foo_mean = interp1d(x_mean, y_mean, bounds_error=False)
        foo_std = interp1d(x_mean, y_std, bounds_error=False)
        foo_ll = interp1d(x_mean, y_ll, bounds_error=False)
        foo_ul = interp1d(x_mean, y_ul, bounds_error=False)
        Y1_mean = foo_mean(data)
        Y1_std = foo_std(data)
        Y1_ll = foo_ll(data)
        Y1_ul = foo_ul(data)
        return (
         Y1_mean, Y1_std, Y1_ll, Y1_ul)

    def _inverse_cdf(self):
        """
        This module will calculate the inverse of CDF 
        which will be used in getting the ensemble of X and Y from
        the ensemble of U and V
        
        The statistics module is used to estimate the CDF, which uses
        kernel methold of cdf estimation
        
        To estimate the inverse of CDF, interpolation method is used, first cdf 
        is estimated at 100 points, now interpolation function is generated 
        to relate cdf at 100 points to data
        """
        x2, x1 = st.cpdf(self.X, kernel='Epanechnikov', n=100)
        self._inv_cdf_x = interp1d(x2, x1)
        y2, y1 = st.cpdf(self.Y, kernel='Epanechnikov', n=100)
        self._inv_cdf_y = interp1d(y2, y1)

    def _integrand_debye(self, t):
        """ 
         Integrand for the first order debye function
         """
        return t / (np.exp(t) - 1)

    def _debye(self, alpha):
        """
        First order Debye function
        """
        return quad(self._integrand_debye, sys.float_info.epsilon, alpha)[0] / alpha

    def _frank_fun(self, alpha):
        """
        optimization of this function will give the parameter for the frank copula
        """
        diff = (1 - self.tau) / 4.0 - (self._debye(-alpha) - 1) / alpha
        return diff ** 2