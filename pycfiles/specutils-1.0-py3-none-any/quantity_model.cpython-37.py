# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nearl/projects/specutils/build/lib/specutils/utils/quantity_model.py
# Compiled at: 2020-01-06 12:55:36
# Size of source mod 2**32: 2503 bytes
from astropy import units as u
__all__ = ['QuantityModel']

class QuantityModel:
    __doc__ = "\n    The QuantityModel was created to wrap `~astropy.modeling.models` that do\n    not have the ability to use `~astropy.units` in the parameters.\n\n    Parameters\n    ----------\n    unitless_model : `~astropy.modeling.Model`\n        A model that does not have units\n\n    input_units : `~astropy.units`\n        Units for the dispersion axis\n\n    return_units : `~astropy.units`\n        Units for the flux axis\n\n    Notes\n    -----\n    When Astropy's modeling is updated so *all* models have the ability\n    to have `~astropy.units.Quantity` on all parameters, then this will\n    not be needed.\n    "

    def __init__(self, unitless_model, input_units, return_units):
        self.unitless_model = unitless_model
        self.__dict__['input_units'] = input_units
        self.__dict__['return_units'] = return_units

    def __hasattr_(self, nm):
        if nm in self.__dict__ or hasattr(self, self.unitless_model):
            return True
        return False

    def __getattr__(self, nm):
        if hasattr(self.unitless_model, nm):
            return getattr(self.unitless_model, nm)
        raise AttributeError("'{}' object has no attribute '{}'".format(self.__class__.__name__, nm))

    def __setattr__(self, nm, val):
        if nm != 'unitless_model' and hasattr(self.unitless_model, nm):
            setattr(self.unitless_model, nm, val)
        else:
            super().__setattr__(nm, val)

    def __delattr__(self, nm):
        if hasattr(self.unitless_model, nm):
            delattr(self.unitless_model, nm)
        else:
            super().__delattr__(nm)

    def __dir__(self):
        thisdir = super().__dir__()
        modeldir = dir(self.unitless_model)
        return sorted(list(thisdir) + list(modeldir))

    def __repr__(self):
        return '<QuantityModel {}, input_units={}, return_units={}>'.format(repr(self.unitless_model)[1:-1], self.input_units, self.return_units)

    def __call__(self, x, *args, **kwargs):
        unitlessx = x.to(self.input_units).value
        result = (self.unitless_model)(unitlessx, *args, **kwargs)
        return u.Quantity(result, (self.return_units), copy=False)