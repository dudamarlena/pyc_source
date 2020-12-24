# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hannu/soft/anaconda/envs/p36/lib/python3.6/site-packages/ldtk/ldmodel.py
# Compiled at: 2016-08-17 11:27:33
# Size of source mod 2**32: 2856 bytes
"""
Limb darkening toolkit
Copyright (C) 2015  Hannu Parviainen <hpparvi@gmail.com>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""
import numpy as np
from numpy import asarray

class LDModel(object):
    npar = None
    name = None
    abbr = None

    def __init__(self):
        raise NotImplementedError

    def __call__(self, mu, pv):
        raise NotImplementedError

    @classmethod
    def eval(cl, mu, pv):
        raise NotImplementedError


class LinearModel(LDModel):
    __doc__ = 'Linear limb darkening model (Mandel & Agol, 2001).'
    npar = 1
    name = 'linear'
    abbr = 'ln'

    @classmethod
    def evaluate(cl, mu, pv):
        assert len(pv) == cl.npar
        mu = asarray(mu)
        return 1.0 - pv[0] * (1.0 - mu)


class QuadraticModel(LDModel):
    __doc__ = 'Quadratic limb darkening model (Kopal, 1950).'
    npar = 2
    name = 'quadratic'
    abbr = 'qd'

    @classmethod
    def evaluate(cl, mu, pv):
        assert len(pv) == cl.npar
        mu = asarray(mu)
        return 1.0 - pv[0] * (1.0 - mu) - pv[1] * (1.0 - mu) ** 2


class SquareRootModel(LDModel):
    __doc__ = 'Square root limb darkening model (van Hamme, 1993).'
    npar = 2
    name = 'sqrt'
    abbr = 'sq'

    @classmethod
    def evaluate(cl, mu, pv):
        assert len(pv) == cl.npar
        mu = asarray(mu)
        return 1.0 - pv[0] * (1.0 - mu) - pv[1] * (1.0 - mu ** 0.5)


class NonlinearModel(LDModel):
    __doc__ = 'Nonlinear limb darkening model (Claret, 2000).'
    npar = 4
    name = 'nonlinear'
    abbr = 'nl'

    @classmethod
    def evaluate(cl, mu, pv):
        assert len(pv) == cl.npar
        mu = asarray(mu)
        return 1.0 - (pv[0] * (1.0 - mu ** 0.5) + pv[1] * (1.0 - mu) + pv[2] * (1.0 - mu ** 1.5) + pv[3] * (1.0 - mu ** 2))


class GeneralModel(LDModel):
    __doc__ = 'General limb darkening model (Gimenez, 2006)'
    npar = None
    name = 'general'
    abbr = 'ge'

    @classmethod
    def evaluate(cl, mu, pv):
        mu = asarray(mu)
        return 1.0 - np.sum([c * (1.0 - mu ** (i + 1)) for i, c in enumerate(pv)], 0)


models = {'linear':LinearModel, 
 'quadratic':QuadraticModel, 
 'sqrt':SquareRootModel, 
 'nonlinear':NonlinearModel, 
 'general':GeneralModel}