# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: signaturesimulator/sense/dielectric/epsmodel.py
# Compiled at: 2018-02-20 04:22:40
"""
Generic model for dielectric mixing models
"""
import numpy as np

class EpsModel(object):

    def __init__(self, **kwargs):
        """
        Parameters
        ----------
        clay : float
            clay content as fractional volume
        sand : float
            sand content as fractional volume
        bulk : float
            bulk density [g/cm**3]; default: 1.65
        mv : float
            volumetric soil moisture content [cm**3/cm**3] = [g/cm**3]
        freq : float
            frequency [GHz]
        """
        self.clay = kwargs.get('clay', None)
        self.sand = kwargs.get('sand', None)
        self.bulk = kwargs.get('bulk', 1.65)
        self.mv = kwargs.get('mv', None)
        self.f = kwargs.get('freq', None)
        self._check()
        return

    def _check(self):
        assert self.clay is not None, 'Clay needs to be provided!'
        assert self.clay >= 0.0
        assert self.clay <= 1.0
        assert self.sand is not None, 'Sand needs to be provided!'
        assert self.sand >= 0.0
        assert self.sand <= 1.0
        assert self.mv is not None, 'volumetric soil moisture needs to be given'
        assert self.f is not None, 'Frequency needs to be given!'
        if isinstance(self.f, np.ndarray):
            assert np.all(self.f > 0.0)
        else:
            assert self.f > 0.0
        return