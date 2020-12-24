# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/mixture/models/optimizers.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 2470 bytes
from pyxrd.generic.models import ChildModel
from pyxrd.calculations.mixture import calculate_mixture, calculate_and_optimize_mixture, get_residual, get_optimized_residual

class Optimizer(ChildModel):
    __doc__ = '\n        A simple model that plugs onto the Mixture model. It provides\n        the functionality related to optimizing the weight fractions, scales\n        and background shifts and residual calculation for the phases.\n    '
    parent_alias = 'mixture'

    def get_current_residual(self):
        """
            Gets the residual for the current mixture solution.
            Convenience function.
        """
        return self.get_residual()

    def get_optimized_residual(self, data_object=None):
        """
            Gets an optimized residual for the current mixture setup. If no
            data_object is passed it is retrieved from the mixture.
        """
        return get_optimized_residual(*self.get_data_object(data_object))[0]

    def get_residual(self, data_object=None):
        """
            Calculates the residual for the given solution in combination with
            the given optimization arguments. If no data_object is passed it is 
            retrieved from the mixture.
        """
        return get_residual(*self.get_data_object(data_object))[0]

    def calculate(self, data_object=None):
        """
            Calculates the total and phase intensities. If no data_object is
            passed it is retrieved from the mixture.
        """
        return calculate_mixture(*self.get_data_object(data_object))

    def optimize(self, data_object=None):
        """
            Optimizes the mixture fractions, scales and bg shifts and returns the
            optimized result. If no data_object is passed it is retrieved from
            the mixture.
        """
        try:
            return calculate_and_optimize_mixture(*self.get_data_object(data_object))
        except AssertionError:
            return

    def get_data_object(self, data_object=None):
        return (
         data_object if data_object is not None else self.parent.data_object,)