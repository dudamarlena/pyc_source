# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/runner/runners/2.166.2/work/1/s/build/lib.macosx-10.9-x86_64-3.5/pycraf/utils/testing.py
# Compiled at: 2020-04-16 04:29:51
# Size of source mod 2**32: 3612 bytes
from __future__ import absolute_import, unicode_literals, division, print_function
from copy import deepcopy
import pytest
from astropy import units as apu
import numpy as np
from .. import conversions as cnv
__all__ = [
 'check_astro_quantities']

def tiny_fraction(num, digit=6):
    """
    Return a tiny fraction of a number (in the specified digit)
    """
    num = np.abs(num)
    num = np.max([num, 1e-30])
    return 10 ** (np.log10(num) - digit)


def check_astro_quantities(func, args_list, kwargs_list=None, invalid_unit=apu.byte):
    if kwargs_list is None:
        kwargs_list = []

    def make_args(alist, klist):
        args = []
        kwargs = {}
        for lowval, hival, unit in args_list:
            if lowval is None and hival is not None:
                lowval = hival
            else:
                if lowval is not None and hival is None:
                    hival = lowval
                elif lowval is None and hival is None:
                    lowval = hival = 0.0
            args.append(np.mean((lowval, hival)) * unit)

        for var, lowval, hival, unit in kwargs_list:
            if lowval is None and hival is not None:
                lowval = hival
            else:
                if lowval is not None and hival is None:
                    hival = lowval
                elif lowval is None and hival is None:
                    lowval = hival = 0.0
            kwargs[var] = np.mean((lowval, hival)) * unit

        return (args, kwargs)

    args, kwargs = make_args(args_list, kwargs_list)
    for case, argtup in enumerate(args_list):
        _args = deepcopy(args)
        inv_lowval = argtup[0]
        if inv_lowval is not None:
            inv_lowval -= tiny_fraction(inv_lowval)
            _args[case] = inv_lowval * _args[case].unit
            with pytest.raises(ValueError):
                func(*_args, **kwargs)
        _args = deepcopy(args)
        inv_hival = argtup[1]
        if inv_hival is not None:
            inv_hival += tiny_fraction(inv_hival)
            _args[case] = inv_hival * _args[case].unit
            with pytest.raises(ValueError):
                func(*_args, **kwargs)
        _args = deepcopy(args)
        _args[case] = _args[case].value * invalid_unit
        with pytest.raises(apu.UnitsError):
            func(*_args, **kwargs)
        _args[case] = _args[case].value
        with pytest.raises(TypeError):
            func(*_args, **kwargs)

    for argtup in kwargs_list:
        _kwargs = deepcopy(kwargs)
        var = argtup[0]
        inv_lowval = argtup[1]
        if inv_lowval is not None:
            inv_lowval -= tiny_fraction(inv_lowval)
            _kwargs[var] = inv_lowval * _kwargs[var].unit
            with pytest.raises(ValueError):
                func(*args, **_kwargs)
        _kwargs = deepcopy(kwargs)
        inv_hival = argtup[2]
        if inv_hival is not None:
            inv_hival += tiny_fraction(inv_hival)
            _kwargs[var] = inv_hival * _kwargs[var].unit
            with pytest.raises(ValueError):
                func(*args, **_kwargs)
        _kwargs = deepcopy(kwargs)
        _kwargs[var] = _kwargs[var].value * invalid_unit
        with pytest.raises(apu.UnitsError):
            func(*args, **_kwargs)
        _kwargs[var] = _kwargs[var].value
        with pytest.raises(TypeError):
            func(*args, **_kwargs)