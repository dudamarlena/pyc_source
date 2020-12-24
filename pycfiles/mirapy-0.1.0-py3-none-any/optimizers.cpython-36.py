# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/swapsha96/mtp/MiraPy/build/lib/mirapy/fitting/optimizers.py
# Compiled at: 2019-05-03 11:14:15
# Size of source mod 2**32: 1086 bytes
from scipy.optimize import minimize
from autograd import grad
from copy import deepcopy

class ParameterEstimation:

    def __init__(self, x, y, model, loss_function, callback=None):
        self.x = x
        self.y = y
        self.init_model = deepcopy(model)
        self.model = deepcopy(model)
        self.p_init = model.get_params_as_array()
        self.loss_function = loss_function
        self.callback = callback
        self.results = None

    def regression_function(self, params):
        self.model.set_params_from_array(params)
        y_true = self.y
        y_pred = self.model(self.x)
        return self.loss_function(y_true, y_pred)

    def get_model(self):
        model = deepcopy(self.init_model)
        if self.results is not None:
            model.set_params_from_array(self.results.x)
        return model

    def fit(self):
        results = minimize((self.regression_function), (self.p_init), method='L-BFGS-B', jac=(grad(self.regression_function)),
          callback=(self.callback))
        self.results = results
        return results