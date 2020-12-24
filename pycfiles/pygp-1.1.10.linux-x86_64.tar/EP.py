# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pygp/likelihood/EP.py
# Compiled at: 2013-04-10 06:45:39
"""
Class with a collection of likelihood functions for EP
- as executation time of this class is an issue we expect the hyperparameters to be set upfront
"""
from numpy import *
import scipy as S, scipy.stats as stats, scipy.special as special

def n2mode(x):
    """convert from natural parameter to mode and back"""
    return array([x[0] / x[1], 1 / x[1]])


def sigmoid(x):
    """sigmoid function int_-inf^+inf Normal(x,1)"""
    return (1 + special.erf(x / S.sqrt(2.0))) / 2.0


def gos(x):
    """Gaussian over sigmoid"""
    return sqrt(2.0 / S.pi) * S.exp(-0.5 * x ** 2) / (1 + special.erf(x / S.sqrt(2.0)))


class ALikelihood(object):
    __slots__ = [
     'logtheta']

    def get_number_of_parameters(self):
        return 0

    def setLogtheta(self, logthetaL):
        assert logthetaL.shape[0] == self.get_number_of_parameters(), 'hyperparameters have wrong shape'
        self.logtheta = logthetaL

    def calcExpectations(self, t, cav_np, x=None):
        """calculate expectation values for EP updates
        t: target
        cav_np: cavitiy distribution (natural parameters)
        x: optional: input
        """
        return


class ProbitLikelihood(ALikelihood):
    """Probit likelihood for GP classification"""

    def get_number_of_parameters(self):
        return 0

    def calcExpectations(self, t, cav_np, x=None):
        """calc expectation values (moments) for EP udpates
        t: the target
        cav_np: (nu,tau) of cavity (natural params)
        x: (optional) input (not used in this likelihood)
        """
        zi = t * cav_np[0] / S.sqrt(cav_np[1] * (1 + cav_np[1]))
        Z = sigmoid(zi)
        Fu = cav_np[0] / cav_np[1] + t * gos(zi) / S.sqrt(cav_np[1] * (1 + cav_np[1]))
        Fs2 = (1 - gos(zi) * (zi + gos(zi)) / (1 + cav_np[1])) / cav_np[1]
        return S.array([Fu, Fs2, Z])


class GaussLikelihood(ALikelihood):
    __slots__ = [
     'sl']

    def get_number_of_parameters(self):
        return 1

    def setLogtheta(self, logthetaL):
        ALikelihood.setLogtheta(self, logthetaL)
        self.sl = exp(2 * logthetaL[0])

    def calcExpectations(self, t, cav_np, x=None):
        """calculate expectation values for EP updates
        t: the target
        cav_np: (nu,tau) of cavity (natural params)
        logthetaL: log hyperparameter for likelihood(std. dev)"""
        cav_mp = n2mode(cav_np)
        stot = self.sl + cav_mp[1]
        Z = stats.norm(cav_mp[0], S.sqrt(stot)).pdf(t)
        C = (1.0 / self.sl + 1.0 / cav_mp[1]) ** (-1)
        Fu = C * (cav_mp[0] / cav_mp[1] + t / self.sl)
        Fs2 = C
        return S.array([Fu, Fs2, Z])


class MOGLikelihood(ALikelihood):
    """Mixture of Gaussian likelihood
    robust likelihood with nm mixture components"""
    __slots__ = [
     'Ncomponents', 'phi', 'sl']

    def __init__(self, Ncomponents=2):
        """MOGLikelihood(Ncomponents=2)
        - mog likelihood with Ncomponents mixture components"""
        self.Ncomponents = Ncomponents

    def get_number_of_parameters(self):
        """get_number_of_parameters; for every mixture components 2 parametrs"""
        return self.Ncomponents * 2

    def setLogtheta(self, logthetaL):
        """set hyperparameter of likelihood :
        logthetaL=log([pi_1,...pi_n,Var_1,..Var_n]
        where pi_i are mixing ratios (sum_pi = 1); and Var_i are the corresponding
        variances of the mixing components"""
        ALikelihood.setLogtheta(self, logthetaL)
        np_2 = self.get_number_of_parameters() / 2
        self.phi = exp(logthetaL[0:np_2])
        self.sl = exp(2 * logthetaL[np_2::])
        return

    def calcExpectations(self, t, cav_np, x=None):
        """calculate expectation values for EP updates
        t: the target
        cav_np: (nu,tau) of cavity (natural params)
        x: (optional) input (not used in this likelihood)
        """
        cav_mp = n2mode(cav_np)
        Z = S.zeros([3])
        dc = S.zeros([3])
        for c in range(self.Ncomponents):
            Sc = self.sl[c] + cav_mp[1]
            dc[0] = self.phi[c] * stats.norm(cav_mp[0], S.sqrt(Sc)).pdf(t)
            dc[1] = dc[0] * (t - cav_mp[0]) * (1.0 / Sc)
            dc[2] = dc[0] * (((t - cav_mp[0]) * (1.0 / Sc)) ** 2 - 1.0 / Sc)
            Z += dc

        alpha = 1.0 / Z[0] * Z[1]
        nu = -(1.0 / Z[0] * Z[2] - alpha ** 2)
        Fu = cav_mp[1] * alpha + cav_mp[0]
        Fs2 = (1 - cav_mp[1] * nu) * cav_mp[1]
        Z = Z[0]
        return S.array([Fu, Fs2, Z])


class ConstrainedLikelihood(ALikelihood):
    """ConstrainedLikelihood:
     - likelihood which allows datapoitns to be constraints rather than full
     datum
     - this likelihood allows to include an alternative ''default'' likelihood, for instance a standard
     Gaussian for non-constrained data entries
     """
    __slots__ = [
     'alt', 'index']

    def __init__(self, alt=GaussLikelihood(), index=-1):
        """ConstarinedLikelihood
        - alt specifies the likelihood function which is used for ''normal'' datums"""
        assert isinstance(alt, ALikelihood), 'alt likelihood needs to be of type ALikelihood'
        self.alt = alt
        self.index = index

    def get_number_of_parameters(self):
        """get_number_of_parameters() returns the number of parameters of the alt likelihood"""
        return self.alt.get_number_of_parameters()

    def setLogtheta(self, logthetaL):
        """set hyperparameter of likelihood :
        - sets hyperparemter in standard likelihood"""
        self.alt.setLogtheta(logthetaL)

    def calcExpectations(self, t, cav_np, x=None):
        """calculate expectation values for EP updates
        t: the target
        cav_np: natural parameter of cavity distribution (nu,tau)
        x: (optional) input (not used in this likelihood)
        """
        cav_mp = n2mode(cav_np)
        Fu = 0
        Fs2 = 0.1
        Z = 0
        mu = cav_mp[0]
        sigma2 = cav_mp[1]
        sigma = S.sqrt(sigma2)
        cav = stats.norm(mu, sigma)
        norm = stats.norm()
        if x[self.index] == 0:
            return self.alt.calcExpectations(t, cav_mp, x)
        if x[self.index] < 0:
            Z = cav.cdf(t)
            alpha = (t - mu) / sigma
            calpha = min(norm.cdf(alpha), 0.9999999999)
            lmb = norm.pdf(alpha) / (1 - calpha)
            delta = lmb * (lmb - alpha)
            Fu = mu - sigma * lmb
            Fs2 = sigma2 * (1 - delta)
        elif x[self.index] > 0:
            Z = cav.cdf(t + 2 * (mu - t))
            alpha = (t - mu) / sigma
            calpha = min(norm.cdf(alpha), 0.9999999999)
            lmb = norm.pdf(alpha) / (1 - calpha)
            delta = lmb * (lmb - alpha)
            Fu = mu + sigma * lmb
            Fs2 = sigma2 * (1 - delta)
        print [mu, sigma, t]
        print [Fu, S.sqrt(Fs2)]
        return S.array([Fu, Fs2, Z])