# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/examples/autoencoder_objective.py
# Compiled at: 2012-10-16 23:54:13
import logging, pickle, scipy
from numpy import *
import theano, theano.tensor as T
from theano import ProfileMode
from theano.gradient import jacobian, hessian
from theano import function, Param, printing
from theano.tensor.shared_randomstreams import RandomStreams

class AutoencoderObjective(object):
    """
        Neural network autoencoder objective function.
        This is a basic autoencoder, no noise is injected, nor is sparsity
        encouraged in any way. Theano is used internally.
    """

    def __init__(self, X, reg, n_hidden, props={}):
        """
            :param X: The dataset stacked as row vectors into a matrix
            :param d: A column vector of class labels (either -1 or 1).
            :param reg: The regulization coefficient. the regulization term is 
            of the form 0.5*reg*||w||^2.
        """
        self.X = X
        self.reg = reg
        self.n = X.shape[0]
        self.m = X.shape[1]
        self.props = props
        self.logger = logging.getLogger('ae')
        self.n_visible = self.m
        self.n_hidden = n_hidden
        self.logger.info('nvisible: %d nhidden: %d', self.n_visible, self.n_hidden)
        self.n_total_weights = self.n_visible + self.n_hidden + self.n_visible * self.n_hidden
        self.buildObjective()

    def unwrap(self, w):
        """
            Extracts three types of parameters from concatenated vector
        """
        bend = self.n_hidden + self.n_visible
        bhid = w[:self.n_hidden]
        bvis = w[self.n_hidden:bend]
        W = w[bend:].reshape((self.n_visible, self.n_hidden))
        return (bhid, bvis, W)

    def buildObjective(self):
        """
            Construct Theano expressions for loss, gradient and gauss-newton mv-multiplication
        """
        p = T.vector(name='p')
        bhid, bvis, W = self.unwrap(p)
        X = T.matrix(name='X')
        y = T.nnet.sigmoid(T.dot(X, W) + bhid)
        zinner = T.dot(y, W.T) + bvis
        z = T.nnet.sigmoid(zinner)
        L = -T.sum(X * T.log(z) + (1 - X) * T.log(1 - z), axis=1)
        loss = T.sum(L) / self.n
        loss += 0.5 * self.reg * T.dot(p, p)
        g = T.grad(loss, p)
        self.obj = function([X, p], (loss, g))
        v = T.vector(name='v')
        Jv = T.Rop(zinner, p, v)
        HJv = T.grad(T.sum(T.grad(loss, zinner) * Jv), zinner, consider_constant=[Jv])
        Gp = T.grad(T.sum(HJv * zinner), p, consider_constant=[HJv, Jv])
        Gp = Gp + self.reg * v
        self.gnprod = function([X, p, v], Gp)

    def __call__(self, w, s=0, e=None):
        if e is None:
            e = self.n
        X = self.X[s:e, :]
        loss, g = self.obj(X, w)
        return (
         loss, g)

    def gaussNewtonProd(self, w, v, s, e):
        Xs = self.X[s:e, :]
        return self.gnprod(Xs, w, v)