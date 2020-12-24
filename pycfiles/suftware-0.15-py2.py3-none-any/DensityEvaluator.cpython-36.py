# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tareen/Desktop/suftware_release_0P13/suftware/src/DensityEvaluator.py
# Compiled at: 2018-04-12 10:53:30
# Size of source mod 2**32: 2770 bytes
import numpy as np
from scipy import interpolate
from suftware.src.utils import check

class DensityEvaluator:
    __doc__ = '\n    A probability density that can be evaluated at anywhere\n\n    Parameters\n    ----------\n\n    field_values: (1D np.array)\n\n        The values of the field used to computed this density.\n\n    grid: (1D np.array)\n\n        The grid points at which the field values are defined. Must be the same\n        the same shape as field.\n\n    Attributes\n    ----------\n\n    field_values:\n        See above.\n\n    grid:\n        See above.\n\n    grid_spacing: (float)\n        The spacing between neighboring gridpoints.\n\n    values: (1D np.array)\n        The values of the probability density at all grid points.\n\n    bounding_box:\n        The domain in which the density is nonzero.\n\n    Z:\n        The normalization constant used to convert the field to a density.\n\n    '

    def __init__(self, field_values, grid, bounding_box, interpolation_method='cubic'):
        self.field_values = field_values
        self.grid = grid
        self.bounding_box = bounding_box
        self.grid_spacing = grid[1] - grid[0]
        self.Z = np.sum(self.grid_spacing * np.exp(-self.field_values))
        self.field_func = interpolate.interp1d((self.grid), (self.field_values),
          kind=interpolation_method,
          bounds_error=False,
          fill_value='extrapolate',
          assume_sorted=True)
        self.values = self.evaluate(xs=(self.grid))

    def evaluate(self, xs):
        """
        Evaluates the probability density at specified positions.

        Note: self(xs) can be used instead of self.evaluate(xs).

        Parameters
        ----------

        xs: (np.array)
            Locations at which to evaluate the density.

        Returns
        -------

        (np.array)
            Values of the density at the specified positions. Values at
            positions outside the bounding box are evaluated to zero.

        """
        values = np.exp(-self.field_func(xs)) / self.Z
        zero_indices = (xs < self.bounding_box[0]) | (xs > self.bounding_box[1])
        values[zero_indices] = 0.0
        return values

    def __call__(self, *args, **kwargs):
        """
        Same as evaluate()
        """
        return (self.evaluate)(*args, **kwargs)