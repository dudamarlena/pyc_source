# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/obpds/material.py
# Compiled at: 2015-11-15 13:26:55
from .units import units, to_units, cm, cm3
import numpy
__all__ = [
 'Material']
k = 8.6173324e-05
N_prefactor = 4829365224630000.0

class Material(object):

    def __init__(self, alloy, doping=None, Na=None, Nd=None):
        """
        Arguments
        ---------
        alloy : openbandparams alloy
            Alloy.
        doping : float
            Ionized dopant concentration (cm**-3).
            Positive for p-type, negative for n-type.
        Na : float
            Ionized acceptor density (cm**-3)
        Nd : float
            Ionized donor density (cm**-3)
        """
        self._Nc_Gamma = {}
        self._Nc_X = {}
        self._Nc_L = {}
        self._Nv = {}
        self._nie = {}
        self._Ei = {}
        self._alloy = alloy
        if doping is not None and Na is not None:
            raise ValueError('If doping is specified, Na cannot be')
        if doping is not None and Nd is not None:
            raise ValueError('If doping is specified, Nd cannot be')
        if doping is not None:
            doping = to_units(doping, 1.0 / cm3)
            if doping >= 0:
                self._Na = doping
                self._Nd = 0.0
            else:
                self._Na = 0
                self._Nd = -doping
        else:
            if Na is not None:
                self._Na = to_units(Na, 1.0 / cm3)
            else:
                self._Na = 0.0
            if Nd is not None:
                self._Nd = to_units(Nd, 1.0 / cm3)
            else:
                self._Nd = 0.0
        self._Nnet = self._Nd - self._Na
        return

    def __getattr__(self, name):
        if hasattr(self._alloy, name):
            return getattr(self._alloy, name)
        raise AttributeError

    def Ei(self, T=300):
        if T in self._Ei:
            return self._Ei[T]
        else:
            Ei = self.Eg() / 2.0 + k * T / 2.0 * numpy.log(self.Nv(T=T) / self.Nc(T=T))
            self._Ei[T] = Ei
            return Ei

    def ni(self, T=300):
        return numpy.sqrt(self.Nv(T=T) * self.Nc(T=T)) * numpy.exp(-self.Eg(T=T) / (2 * k * T))

    def Nc_Gamma(self, T=300):
        if T in self._Nc_Gamma:
            return self._Nc_Gamma[T]
        else:
            meff = self.meff_e_Gamma(T=T)
            Nc = N_prefactor * (meff * T) ** 1.5
            self._Nc_Gamma[T] = Nc
            return Nc

    def Nc_L(self, T=300):
        if T in self._Nc_L:
            return self._Nc_L[T]
        else:
            meff = self.meff_e_L_DOS(T=T)
            Nc = N_prefactor * (meff * T) ** 1.5
            self._Nc_L[T] = Nc
            return Nc

    def Nc_X(self, T=300):
        if T in self._Nc_X:
            return self._Nc_X[T]
        else:
            meff = self.meff_e_X_DOS(T=T)
            Nc = N_prefactor * (meff * T) ** 1.5
            self._Nc_X[T] = Nc
            return Nc

    def Nc(self, T=300.0):
        Eg_Gamma = self.Eg_Gamma(T=T)
        Eg_X = self.Eg_X(T=T)
        Eg_L = self.Eg_L(T=T)
        if Eg_Gamma < Eg_X:
            if Eg_Gamma < Eg_L:
                return self.Nc_Gamma()
            else:
                return self.Nc_L()

        else:
            if Eg_X < Eg_L:
                return self.Nc_X()
            else:
                return self.Nc_L()

    def Nv(self, T=300.0):
        if T in self._Nv:
            return self._Nv[T]
        else:
            meff = self.meff_h_DOS(T=T)
            Nv = N_prefactor * (meff * T) ** 1.5
            self._Nv[T] = Nv
            return Nv

    def meff_h_DOS(self, T=300.0):
        return self.meff_hh_100(T=T)

    def Na(self, **kwargs):
        """Returns the ionized acceptor concentration, Na (cm**-3)"""
        return self._Na

    def Nd(self, **kwargs):
        """Returns the ionized donor concentration, Nd (cm**-3)"""
        return self._Nd

    def Nnet(self, **kwargs):
        """Returns the net fixed charge, Nnet (cm**-3)"""
        return self._Nnet