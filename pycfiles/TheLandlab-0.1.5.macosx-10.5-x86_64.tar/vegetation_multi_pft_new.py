# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /anaconda/lib/python2.7/site-packages/landlab/components/single_vegetation/vegetation_multi_pft_new.py
# Compiled at: 2015-03-08 15:33:09
from landlab import Component
import numpy as np
_VALID_METHODS = set(['Grid'])

def assert_method_is_valid(method):
    if method not in _VALID_METHODS:
        raise ValueError('%s: Invalid method name' % method)


class Vegetation(Component):
    """1D and 2D vegetation dynamics.

    Landlab component that implements 1D and 2D vegetation dynamics model.
    """
    _name = 'Vegetation'
    _input_var_names = set([
     'ActualEvapotranspiration',
     'WaterStress',
     'PotentialEvapotranspiration'])
    _output_var_names = set([
     'LiveLeafAreaIndex',
     'DeadLeafAreaIndex',
     'VegetationCover',
     'LiveBiomass',
     'DeadBiomass'])
    _var_units = {'LiveLeafAreaIndex': 'None', 
       'DeadLeafAreaIndex': 'None', 
       'VegetationCover': 'None', 
       'ActualEvapotranspiration': 'mm', 
       'PotentialEvapotranspiration': 'mm', 
       'WaterStress': 'Pa', 
       'LiveBiomass': 'g DM m^-2 d^-1', 
       'DeadBiomass': 'g DM m^-2 d^-1'}

    def __init__(self, grid, data, **kwds):
        self._method = kwds.pop('method', 'Grid')
        assert_method_is_valid(self._method)
        super(Vegetation, self).__init__(grid)
        self.initialize(data, VEGTYPE=grid['cell']['VegetationType'], **kwds)
        for name in self._input_var_names:
            if name not in self.grid.at_cell:
                self.grid.add_zeros('cell', name, units=self._var_units[name])

        for name in self._output_var_names:
            if name not in self.grid.at_cell:
                self.grid.add_zeros('cell', name, units=self._var_units[name])

        self._cell_values = self.grid['cell']
        self._Blive_ini = self._Blive_init * np.ones(self.grid.number_of_cells)
        self._Bdead_ini = self._Bdead_init * np.ones(self.grid.number_of_cells)

    def initialize(self, data, **kwds):
        self._vegtype = kwds.pop('VEGTYPE', np.zeros(self.grid.number_of_cells, dtype=int))
        self._WUE = np.choose(self._vegtype, kwds.pop('WUE', [
         data['WUE_grass'], data['WUE_shrub'], data['WUE_tree'],
         data['WUE_bare'], data['WUE_shrub'], data['WUE_tree']]))
        self._LAI_max = np.choose(self._vegtype, kwds.pop('LAI_MAX', [
         data['LAI_MAX_grass'], data['LAI_MAX_shrub'],
         data['LAI_MAX_tree'], data['LAI_MAX_bare'],
         data['LAI_MAX_shrub'], data['LAI_MAX_tree']]))
        self._cb = np.choose(self._vegtype, kwds.pop('CB', [
         data['CB_grass'], data['CB_shrub'], data['CB_tree'],
         data['CB_bare'], data['CB_shrub'], data['CB_tree']]))
        self._cd = np.choose(self._vegtype, kwds.pop('CD', [
         data['CD_grass'], data['CD_shrub'], data['CD_tree'],
         data['CD_bare'], data['CD_shrub'], data['CD_tree']]))
        self._ksg = np.choose(self._vegtype, kwds.pop('KSG', [
         data['KSG_grass'], data['KSG_shrub'], data['KSG_tree'],
         data['KSG_bare'], data['KSG_shrub'], data['KSG_tree']]))
        self._kdd = np.choose(self._vegtype, kwds.pop('KDD', [
         data['KDD_grass'], data['KDD_shrub'], data['KDD_tree'],
         data['KDD_bare'], data['KDD_shrub'], data['KDD_tree']]))
        self._kws = np.choose(self._vegtype, kwds.pop('KWS', [
         data['KWS_grass'], data['KWS_shrub'], data['KWS_tree'],
         data['KWS_bare'], data['KWS_shrub'], data['KWS_tree']]))
        self._Blive_init = kwds.pop('BLIVE_INI', data['BLIVE_INI'])
        self._Bdead_init = kwds.pop('BDEAD_INI', data['BDEAD_INI'])
        self._ETthresholdup = kwds.pop('ETTup', data['ETTup'])
        self._ETthresholddown = kwds.pop('ETTdwn', data['ETTdwn'])
        self._cell_values = self.grid['cell']

    def update(self, **kwds):
        PETthreshold_ = kwds.pop('PotentialEvapotranspirationThreshold', 0)
        Tb = kwds.pop('Tb', 24.0)
        Tr = kwds.pop('Tr', 0.01)
        PET = self._cell_values['PotentialEvapotranspiration']
        ActualET = self._cell_values['ActualEvapotranspiration']
        Water_stress = self._cell_values['WaterStress']
        self._LAIlive = self._cell_values['LiveLeafAreaIndex']
        self._LAIdead = self._cell_values['DeadLeafAreaIndex']
        self._Blive = self._cell_values['LiveBiomass']
        self._Bdead = self._cell_values['DeadBiomass']
        self._VegCov = self._cell_values['VegetationCover']
        if PETthreshold_ == 1:
            PETthreshold = self._ETthresholdup
        else:
            PETthreshold = self._ETthresholddown
        for cell in range(0, self.grid.number_of_cells):
            WUE = self._WUE[cell]
            LAImax = self._LAI_max[cell]
            cb = self._cb[cell]
            cd = self._cd[cell]
            ksg = self._ksg[cell]
            kdd = self._kdd[cell]
            kws = self._kws[cell]
            LAIlive = min(cb * self._Blive_ini[cell], LAImax)
            LAIdead = min(cd * self._Bdead_ini[cell], LAImax - LAIlive)
            NPP = max(ActualET[cell] / (Tb + Tr) * WUE * 24.0 * 0.55 * 1000, 0.001)
            if self._vegtype[cell] == 0:
                if PET[cell] > PETthreshold:
                    Bmax = (LAImax - LAIdead) / cb
                    Yconst = 1 / (1 / Bmax + (kws * Water_stress[cell] + ksg) / NPP)
                    Blive = (self._Blive_ini[cell] - Yconst) * np.exp(-(NPP / Yconst) * ((Tb + Tr) / 24.0)) + Yconst
                    Bdead = (self._Bdead_ini[cell] + (Blive - max(Blive * np.exp(-ksg * Tb / 24.0), 1e-05))) * np.exp(-kdd * min(PET[cell] / 10.0, 1.0) * Tb / 24.0)
                else:
                    Blive = max(self._Blive_ini[cell] * np.exp(-2 * ksg * Tb / 24.0), 1)
                    Bdead = max((self._Bdead_ini[cell] + (self._Blive_ini[cell] - max(self._Blive_ini[cell] * np.exp(-2 * ksg * Tb / 24.0), 1e-06))) * np.exp(-1 * kdd * min(PET[cell] / 10.0, 1.0) * Tb / 24.0), 0.0)
            elif self._vegtype[cell] == 3:
                Blive = 0.0
                Bdead = 0.0
            else:
                Bmax = LAImax / cb
                Yconst = 1 / (1 / Bmax + (kws * Water_stress[cell] + ksg) / NPP)
                Blive = (self._Blive_ini[cell] - Yconst) * np.exp(-(NPP / Yconst) * ((Tb + Tr) / 24.0)) + Yconst
                Bdead = (self._Bdead_ini[cell] + (Blive - max(Blive * np.exp(-ksg * Tb / 24.0), 1e-05))) * np.exp(-kdd * min(PET[cell] / 10.0, 1.0) * Tb / 24.0)
            LAIlive = min(cb * (Blive + self._Blive_ini[cell]) / 2.0, LAImax)
            LAIdead = min(cd * (Bdead + self._Bdead_ini[cell]) / 2.0, LAImax - LAIlive)
            if self._vegtype[cell] == 0:
                Vt = 1.0 - np.exp(-0.75 * (LAIlive + LAIdead))
            else:
                Vt = 1.0
            self._LAIlive[cell] = LAIlive
            self._LAIdead[cell] = LAIdead
            self._VegCov[cell] = Vt
            self._Blive[cell] = Blive
            self._Bdead[cell] = Bdead

        self._Blive_ini = self._Blive
        self._Bdead_ini = self._Bdead