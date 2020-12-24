# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\vanilla_option_pricing\calibration.py
# Compiled at: 2018-09-15 10:52:38
# Size of source mod 2**32: 2149 bytes
import pandas as pd
from scipy.optimize import minimize

class ModelCalibration:
    __doc__ = '\n    Calibrate option pricing models according to prices of listed options\n\n    :param options: a collection of :class:`~option.VanillaOption`\n    '
    DEFAULT_PARAMETER_LOWER_BOUND = 0.0001

    def __init__(self, options):
        self.options = options

    def calibrate_model(self, model, method=None, options=None, bounds='default'):
        """
        Tune model parameters and returns a tuned model. The algorithm tries to minimize the squared difference
        between the prices of listed options and the prices predicted by the model, by tuning model parameters.
        The numerical optimization is performed by :func:`~scipy.optimize.minimize` in the scipy package.

        :param model: the model to calibrate
        :param method: see :func:`~scipy.optimize.minimize`
        :param options: see :func:`~scipy.optimize.minimize`
        :param bounds: the bounds to apply to parameters. If none is specified, then the
                       :attr:`~DEFAULT_PARAMETER_LOWER_BOUND` is applied for all the parameters.
                       Otherwise, a list of tuples (lower_bound, upper_bound) for each parameter shall be specified.
        :return: a tuple (res, model), where res is the result of :func:`~scipy.optimize.minimize`,
                 while res a calibrated model
        """
        if bounds == 'default':
            bounds = (
             (
              self.DEFAULT_PARAMETER_LOWER_BOUND, None),) * len(model.parameters)
        loss = self._get_loss_function(model)
        res = minimize(loss, (model.parameters), bounds=bounds, method=method, options=options)
        model.parameters = res.x
        return (res, model)

    def _get_loss_function(self, model):

        def _loss_function(parameters):
            model.parameters = parameters
            predicted_prices = pd.Series([model.price_option_black(o) for o in self.options])
            real_prices = pd.Series([o.price for o in self.options])
            return sum((predicted_prices - real_prices) ** 2)

        return _loss_function