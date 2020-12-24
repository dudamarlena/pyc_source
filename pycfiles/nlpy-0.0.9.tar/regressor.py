# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hadoop/nlpy/nlpy/deep/networks/regressor.py
# Compiled at: 2014-12-02 21:02:27
from theano import tensor as T, tensor
from nlpy.deep import NeuralNetwork

class NeuralRegressor(NeuralNetwork):
    """A regressor attempts to produce a target output."""

    def setup_vars(self):
        super(NeuralRegressor, self).setup_vars()
        self.vars.k = T.matrix('k')
        self.inputs.append(self.vars.k)

    @property
    def cost(self):
        err = self.vars.y - self.vars.k
        return T.mean((err * err).sum(axis=1))


class SimpleRegressor(NeuralNetwork):
    """A regressor attempts to produce a target output."""

    def setup_vars(self):
        super(SimpleRegressor, self).setup_vars()
        self.vars.k = T.dvector('k')
        self.inputs.append(self.vars.k)

    @property
    def cost(self):
        err = self.vars.y[:, 0] - self.vars.k
        return T.mean(err * err)