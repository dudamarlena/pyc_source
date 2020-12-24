# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/shu/research/deepy/deepy/networks/regressor.py
# Compiled at: 2016-04-20 00:05:45
from theano import tensor as T
from . import NeuralNetwork
from deepy.utils import dim_to_var, RegressionCost

class NeuralRegressor(NeuralNetwork):
    """
    A class of defining stacked neural network regressors.
    """

    def __init__(self, input_dim, target_tensor=2, clip_value=None, input_tensor=None):
        self.target_tensor = dim_to_var(target_tensor, 'k') if type(target_tensor) == int else target_tensor
        self.clip_value = clip_value
        super(NeuralRegressor, self).__init__(input_dim, input_tensor=input_tensor)

    def setup_variables(self):
        super(NeuralRegressor, self).setup_variables()
        self.k = self.target_tensor
        self.target_variables.append(self.k)

    def _cost_func(self, y):
        if self.clip_value:
            y = T.clip(y, -self.clip_value, self.clip_value)
        return RegressionCost(y, self.k).get()

    @property
    def cost(self):
        return self._cost_func(self.output)

    @property
    def test_cost(self):
        return self._cost_func(self.test_output)