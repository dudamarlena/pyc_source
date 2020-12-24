# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\pycker\quantity_error.py
# Compiled at: 2017-09-14 05:04:09
# Size of source mod 2**32: 4892 bytes
"""
Author: Keurfon Luu <keurfon.luu@mines-paristech.fr>
License: MIT
"""
import numpy as np
__all__ = [
 'QuantityError']

class QuantityError:
    __doc__ = '\n    Uncertainty information for a physical quantity.\n    \n    Parameters\n    ----------\n    uncertainty : scalar or None, default None\n        Uncertainty as the absolute value of symmetric deviation from the main\n        value.\n    lower_uncertainty : scalar or None, default None\n        Uncertainty as the absolute value of deviation from the main value\n        towards smaller values.\n    upper_uncertainty : scalar or None, default None\n        Uncertainty as the absolute value of deviation from the main value\n        towards larger values.\n    confidence_level : scalar or None, default None\n        Confidence level of the uncertainty, given in percent (0-100).\n    '
    _ATTRIBUTES = [
     'uncertainty', 'lower_uncertainty', 'upper_uncertainty', 'confidence_level']

    def __init__(self, uncertainty=None, lower_uncertainty=None, upper_uncertainty=None, confidence_level=None):
        if uncertainty is not None and (not isinstance(uncertainty, (int, float)) or uncertainty < 0.0):
            raise ValueError('uncertainty must be a positive scalar')
        else:
            self._uncertainty = uncertainty
        if lower_uncertainty is not None and not isinstance(lower_uncertainty, (int, float)):
            raise ValueError('lower_uncertainty must be a scalar')
        else:
            self._lower_uncertainty = lower_uncertainty
        if upper_uncertainty is not None and not isinstance(upper_uncertainty, (int, float)):
            raise ValueError('upper_uncertainty must be a scalar')
        else:
            self._upper_uncertainty = upper_uncertainty
        if confidence_level is not None and (not isinstance(confidence_level, (int, float)) or confidence_level < 0.0 or confidence_level > 100.0):
            raise ValueError('confidence_level must be a scalar in [ 0., 100. ]')
        else:
            self._confidence_level = confidence_level

    def __repr__(self):
        uncertainty = '%s: %s' % ('uncertainty', self._print_attr('uncertainty'))
        if self._lower_uncertainty is not None and self._upper_uncertainty is not None:
            uncertainty += ', lower: %s, upper: %s' % (self._print_attr('lower_uncertainty'), self._print_attr('upper_uncertainty'))
        return 'QuantityError(%s)' % uncertainty

    def _print_attr(self, attr):
        if attr not in self._ATTRIBUTES:
            raise ValueError("error_type should be either 'uncertainty', 'lower_uncertainty', 'upper_uncertainty' or 'confidence_level'")
        else:
            if attr == 'uncertainty':
                return self._uncertainty
            if attr == 'lower_uncertainty':
                return self._lower_uncertainty
            if attr == 'upper_uncertainty':
                return self._upper_uncertainty
            if attr == 'confidence_level':
                return self._confidence_level

    def toarray(self):
        """
        Save attributes to array.
        
        Returns
        -------
        arr : ndarray
            Output array.
        """
        return np.array([self._uncertainty, self._lower_uncertainty, self._upper_uncertainty, self._confidence_level])

    @property
    def uncertainty(self):
        """
        scalar or None
        Uncertainty as the absolute value of symmetric deviation from the main
        value.
        """
        return self._uncertainty

    @uncertainty.setter
    def uncertainty(self, value):
        self._uncertainty = value

    @property
    def lower_uncertainty(self):
        """
        scalar or None
        Uncertainty as the absolute value of deviation from the main value
        towards smaller values.
        """
        return self._lower_uncertainty

    @lower_uncertainty.setter
    def lower_uncertainty(self, value):
        self._lower_uncertainty = value

    @property
    def upper_uncertainty(self):
        """
        scalar or None
        Uncertainty as the absolute value of deviation from the main value
        towards larger values.
        """
        return self._upper_uncertainty

    @upper_uncertainty.setter
    def upper_uncertainty(self, value):
        self._upper_uncertainty = value

    @property
    def confidence_level(self):
        """
        scalar or None
        Confidence level of the uncertainty, given in percent (0-100).
        """
        return self._confidence_level

    @confidence_level.setter
    def confidence_level(self, value):
        self._confidence_level = value