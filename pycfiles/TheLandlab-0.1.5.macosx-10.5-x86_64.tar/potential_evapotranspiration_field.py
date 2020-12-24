# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /anaconda/lib/python2.7/site-packages/landlab/components/PET/potential_evapotranspiration_field.py
# Compiled at: 2015-03-08 15:33:09
from landlab import Component
import numpy as np
_VALID_METHODS = set(['Constant', 'PriestlyTaylor', 'MeasuredRadiationPT',
 'Cosine'])

def assert_method_is_valid(method):
    if method not in _VALID_METHODS:
        raise ValueError('%s: Invalid method name' % method)


class PotentialEvapotranspiration(Component):
    """
    Landlab component that calculates Potential Evapotranspiration.

    Examples
    --------
    >>> from landlab import RasterModelGrid
    >>> from landlab.components.PET.potential_evapotranspiration_field import PotentialEvapotranspiration

    >>> grid = RasterModelGrid(5, 4, 1.e4)
    >>> PET = PotentialEvapotranspiration(grid)
    >>> PET.name
    'Potential Evapotranspiration'
    """
    _name = 'Potential Evapotranspiration'
    _input_var_names = set([
     'RadiationFactor'])
    _output_var_names = set([
     'TotalShortWaveRadiation',
     'NetShortWaveRadiation',
     'NetLongWaveRadiation',
     'NetRadiation',
     'PotentialEvapotranspiration'])
    _var_units = {'PotentialEvapotranspiration': 'mm', 
       'TotalShortWaveRadiation': 'W/m^2', 
       'NetShortWaveRadiation': 'W/m^2', 
       'NetLongWaveRadiation': 'W/m^2', 
       'NetRadiation': 'W/m^2', 
       'RadiationFactor': 'None'}

    def __init__(self, grid, **kwds):
        self._method = kwds.pop('method', 'Constant')
        self._alpha = kwds.pop('PriestlyTaylorConstant', 1.26)
        self._a = kwds.pop('Albedo', 0.6)
        self._pwhv = kwds.pop('LatentHeatofVaporization', 28.34)
        self._y = kwds.pop('PsychometricConstant', 0.066)
        self._sigma = kwds.pop('StefanBoltzmannConstant', 5.67e-08)
        self._Gsc = kwds.pop('SolarConstant', 1366.67)
        self._phi = 3.14 / 180 * kwds.pop('Latitude', 34.0)
        self._z = kwds.pop('ElevationofMeasurement', 300)
        self._Krs = kwds.pop('AdjustmentCoefficient', 0.18)
        self._LT = kwds.pop('LT', 0.0)
        self._ND = kwds.pop('ND', 365.0)
        self._TmaxF_mean = kwds.pop('MeanTmaxF', 12.0)
        self._DeltaD = kwds.pop('DeltaD', 5.0)
        assert_method_is_valid(self._method)
        super(PotentialEvapotranspiration, self).__init__(grid, **kwds)
        for name in self._input_var_names:
            if name not in self.grid.at_cell:
                self.grid.add_zeros('cell', name, units=self._var_units[name])

        for name in self._output_var_names:
            if name not in self.grid.at_cell:
                self.grid.add_zeros('cell', name, units=self._var_units[name])

        self._cell_values = self.grid['cell']

    def update(self, current_time, **kwds):
        if self._method == 'Constant':
            self._PET_value = kwds.pop('ConstantPotentialEvapotranspiration', 12.0)
        elif self._method == 'PriestlyTaylor':
            Tmin = kwds.pop('Tmin', 0.0)
            Tmax = kwds.pop('Tmax', 1.0)
            Tavg = kwds.pop('Tavg', 0.5)
            self._PET_value = self.PriestlyTaylor(current_time, Tmax, Tmin, Tavg)
            self._cell_values['TotalShortWaveRadiation'] = self._Rs * self._cell_values['RadiationFactor']
            self._cell_values['NetShortWaveRadiation'] = self._Rns * self._cell_values['RadiationFactor']
            self._cell_values['NetLongWaveRadiation'] = self._Rnl * self._cell_values['RadiationFactor']
            self._cell_values['NetRadiation'] = self._Rn * self._cell_values['RadiationFactor']
        elif self._method == 'MeasuredRadiationPT':
            Tavg = kwds.pop('Tavg', 0.5)
            Robs = kwds.pop('Radiation', 350.0)
            self._PET_value = self.MeasuredRadPT(Tavg, (1 - self._a) * Robs)
        elif self._method == 'Cosine':
            self._J = np.floor((current_time - np.floor(current_time)) * 365.0)
            self._PET_value = max(self._TmaxF_mean + self._DeltaD / 2.0 * np.cos(2 * np.pi * (self._J - self._LT - self._ND / 2) / self._ND), 0.0)
        self._PET = self._PET_value * self._cell_values['RadiationFactor']
        self._cell_values['PotentialEvapotranspiration'] = self._PET

    def PriestlyTaylor(self, current_time, Tmax, Tmin, Tavg):
        """
            Julian Day - ASCE-EWRI Task Committee Report, Jan-2005 - Eqn 25, (52)
        """
        self._J = np.floor((current_time - np.floor(current_time)) * 365)
        self._es = 0.6108 * np.exp(17.27 * Tavg / (237.7 + Tavg))
        self._ea = 0.6108 * np.exp(17.27 * Tmin / (237.7 + Tmin))
        self._delta = 4098.0 * self._es / (237.3 + Tavg) ** 2.0
        self._sdecl = 0.409 * np.sin(6.28 / 365.0 * self._J - 1.39)
        self._dr = 1 + 0.033 * np.cos(6.28 / 365.0 * self._J)
        self._x = 1.0 - np.tan(self._phi) ** 2.0 * np.tan(self._sdecl) ** 2.0
        if self._x <= 0:
            self._x = 1e-05
        self._ws = 3.14 / 2.0 - np.arctan(-1 * np.tan(self._phi) * np.tan(self._sdecl) / self._x ** 2.0)
        self._Ra = 11.57 * (24.0 / 3.14) * 4.92 * self._dr * (self._ws * np.sin(self._phi) * np.sin(self._sdecl) + np.cos(self._phi) * np.cos(self._sdecl) * np.sin(self._ws))
        self._Rso = (0.75 + 2.0 * 1e-05 * self._z) * self._Ra
        self._Rs = min(self._Krs * self._Ra * np.sqrt(Tmax - Tmin), self._Rso)
        self._Rns = self._Rs * (1 - self._a)
        if self._Rso > 0:
            self._u = self._Rs / self._Rso
        else:
            self._u = 0
        if self._u < 0.3:
            self._u = 0.3
        elif self._u > 1:
            self._u = 1.0
        self._fcd = 1.35 * self._u - 0.35
        self._Rnl = self._sigma * self._fcd * (0.34 - 0.14 * np.sqrt(self._ea) * (((Tmax + 273.16) ** 4.0 + (Tmin + 273.16) ** 4.0) / 2.0))
        self._Rn = self._Rns - self._Rnl
        self._ETp = max(self._alpha * (self._delta / (self._delta + self._y)) * (self._Rn / self._pwhv), 0)
        return self._ETp

    def MeasuredRadPT(self, Tavg, Rnobs):
        """
            Saturation Vapor Pressure - ASCE-EWRI Task Committee Report, Jan-2005 - Eqn 6, (37)
        """
        self._es = 0.6108 * np.exp(17.27 * Tavg / (237.7 + Tavg))
        self._delta = 4098.0 * self._es / (237.3 + Tavg) ** 2.0
        self._ETp = max(self._alpha * (self._delta / (self._delta + self._y)) * (Rnobs / self._pwhv), 0)
        return self._ETp