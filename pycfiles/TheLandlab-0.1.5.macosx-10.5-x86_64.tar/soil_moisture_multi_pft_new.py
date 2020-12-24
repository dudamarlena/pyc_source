# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /anaconda/lib/python2.7/site-packages/landlab/components/soil_moisture/soil_moisture_multi_pft_new.py
# Compiled at: 2015-03-08 15:33:09
from landlab import Component
import numpy as np
_VALID_METHODS = set(['Grid', 'Multi'])

def assert_method_is_valid(method):
    if method not in _VALID_METHODS:
        raise ValueError('%s: Invalid method name' % method)


class SoilMoisture(Component):
    _name = 'Soil Moisture'
    _input_var_names = set([
     'VegetationCover',
     'LiveLeafAreaIndex',
     'PotentialEvapotranspiraton'])
    _output_var_names = set([
     'WaterStress',
     'SaturationFraction',
     'Drainage',
     'Runoff',
     'ActualEvapotranspiration'])
    _var_units = {'VegetationCover': 'None', 
       'LiveLeafAreaIndex': 'None', 
       'PotentialEvapotranspiraton': 'mm', 
       'WaterStress': 'Pa', 
       'SaturationFraction': 'None', 
       'Drainage': 'mm', 
       'Runoff': 'mm', 
       'ActualEvapotranspiration': 'mm'}

    def __init__(self, grid, data, **kwds):
        self._method = kwds.pop('method', 'Grid')
        assert_method_is_valid(self._method)
        super(SoilMoisture, self).__init__(grid)
        self.initialize(data, VEGTYPE=grid['cell']['VegetationType'], **kwds)
        for name in self._input_var_names:
            if name not in self.grid.at_cell:
                self.grid.add_zeros('cell', name, units=self._var_units[name])

        for name in self._output_var_names:
            if name not in self.grid.at_cell:
                self.grid.add_zeros('cell', name, units=self._var_units[name])

        self._nodal_values = self.grid['node']
        if 'InitialSaturationFraction' not in self.grid.at_cell:
            self.grid.add_zeros('cell', 'InitialSaturationFraction', units='None')
        self._cell_values = self.grid['cell']

    def initialize(self, data, **kwds):
        self._vegtype = kwds.pop('VEGTYPE', np.zeros(self.grid.number_of_cells, dtype=int))
        self._runon = kwds.pop('RUNON', 0.0)
        self._fbare = kwds.pop('F_BARE', 0.7)
        self._interception_cap = np.choose(self._vegtype, kwds.pop('INTERCEPT_CAP', [
         data['INTERCEPT_CAP_grass'], data['INTERCEPT_CAP_shrub'],
         data['INTERCEPT_CAP_tree'], data['INTERCEPT_CAP_bare'],
         data['INTERCEPT_CAP_shrub'], data['INTERCEPT_CAP_tree']]))
        self._zr = np.choose(self._vegtype, kwds.pop('ZR', [
         data['ZR_grass'], data['ZR_shrub'], data['ZR_tree'],
         data['ZR_bare'], data['ZR_shrub'], data['ZR_tree']]))
        self._soil_Ib = np.choose(self._vegtype, kwds.pop('I_B', [
         data['I_B_grass'], data['I_B_shrub'], data['I_B_tree'],
         data['I_B_bare'], data['I_B_shrub'], data['I_B_tree']]))
        self._soil_Iv = np.choose(self._vegtype, kwds.pop('I_V', [
         data['I_V_grass'], data['I_V_shrub'], data['I_V_tree'],
         data['I_V_bare'], data['I_V_shrub'], data['I_V_tree']]))
        self._soil_Ew = kwds.pop('EW', [0.1])
        self._soil_pc = np.choose(self._vegtype, kwds.pop('PC', [
         data['PC_grass'], data['PC_shrub'], data['PC_tree'],
         data['PC_bare'], data['PC_shrub'], data['PC_tree']]))
        self._soil_fc = np.choose(self._vegtype, kwds.pop('FC', [
         data['FC_grass'], data['FC_shrub'], data['FC_tree'],
         data['FC_bare'], data['FC_shrub'], data['FC_tree']]))
        self._soil_sc = np.choose(self._vegtype, kwds.pop('SC', [
         data['SC_grass'], data['SC_shrub'], data['SC_tree'],
         data['SC_bare'], data['SC_shrub'], data['SC_tree']]))
        self._soil_wp = np.choose(self._vegtype, kwds.pop('WP', [
         data['WP_grass'], data['WP_shrub'], data['WP_tree'],
         data['WP_bare'], data['WP_shrub'], data['WP_tree']]))
        self._soil_hgw = np.choose(self._vegtype, kwds.pop('HGW', [
         data['HGW_grass'], data['HGW_shrub'], data['HGW_tree'],
         data['HGW_bare'], data['HGW_shrub'], data['HGW_tree']]))
        self._soil_beta = np.choose(self._vegtype, kwds.pop('BETA', [
         data['BETA_grass'], data['BETA_shrub'], data['BETA_tree'],
         data['BETA_bare'], data['BETA_shrub'], data['BETA_tree']]))
        self._LAI_max = np.choose(self._vegtype, kwds.pop('LAI_MAX', [
         data['LAI_MAX_grass'], data['LAI_MAX_shrub'],
         data['LAI_MAX_tree'], data['LAI_MAX_bare'],
         data['LAI_MAX_shrub'], data['LAI_MAX_tree']]))

    def update(self, current_time, **kwds):
        P = kwds.pop('P', 5.0)
        Tb = kwds.pop('Tb', 24.0)
        Tr = kwds.pop('Tr', 0.0)
        self._PET = self._cell_values['PotentialEvapotranspiration']
        self._SO = self._cell_values['InitialSaturationFraction']
        self._vegcover = self._cell_values['VegetationCover']
        self._water_stress = self._cell_values['WaterStress']
        self._S = self._cell_values['SaturationFraction']
        self._D = self._cell_values['Drainage']
        self._ETA = self._cell_values['ActualEvapotranspiration']
        self._fr = self._cell_values['LiveLeafAreaIndex'] / self._LAI_max
        self._fr[self._fr > 1.0] = 1.0
        self._Sini = np.zeros(self._SO.shape)
        self._ETmax = np.zeros(self._SO.shape)
        for cell in range(0, self.grid.number_of_cells):
            s = self._SO[cell]
            fbare = self._fbare
            ZR = self._zr[cell]
            pc = self._soil_pc[cell]
            fc = self._soil_fc[cell]
            sc = self._soil_sc[cell]
            wp = self._soil_wp[cell]
            hgw = self._soil_hgw[cell]
            beta = self._soil_beta[cell]
            Inf_cap = self._soil_Ib[cell] * (1 - self._vegcover[cell]) + self._soil_Iv[cell] * self._vegcover[cell]
            Int_cap = min(self._vegcover[cell] * self._interception_cap[cell], P * self._vegcover[cell])
            Peff = max(P - Int_cap, 0.0)
            mu = Inf_cap / 1000.0 / (pc * ZR * (np.exp(beta * (1.0 - fc)) - 1.0))
            Ep = max(self._PET[cell] * self._fr[cell] + fbare * self._PET[cell] * (1.0 - self._fr[cell]) - Int_cap, 0.0001)
            self._ETmax[cell] = Ep
            nu = Ep / 24.0 / 1000.0 / (pc * ZR)
            nuw = Ep * 0.1 / 24.0 / 1000.0 / (pc * ZR)
            sini = self._SO[cell] + (Peff + self._runon) / (pc * ZR * 1000.0)
            if sini > 1.0:
                self._runoff = (sini - 1.0) * pc * ZR * 1000.0
                sini = 1.0
            else:
                self._runoff = 0.0
            if sini >= fc:
                tfc = 1.0 / (beta * (mu - nu)) * (beta * (fc - sini) + np.log((nu - mu + mu * np.exp(beta * (sini - fc))) / nu))
                tsc = (fc - sc) / nu + tfc
                twp = (sc - wp) / (nu - nuw) * np.log(nu / nuw) + tsc
                if Tb < tfc:
                    s = abs(sini - 1.0 / beta * np.log(((nu - mu + mu * np.exp(beta * (sini - fc))) * np.exp(beta * (nu - mu) * Tb) - mu * np.exp(beta * (sini - fc))) / (nu - mu)))
                    self._D[cell] = pc * ZR * 1000.0 * (sini - s) - Tb * (Ep / 24.0)
                    self._ETA[cell] = Tb * (Ep / 24.0)
                elif Tb >= tfc and Tb < tsc:
                    s = fc - nu * (Tb - tfc)
                    self._D[cell] = pc * ZR * 1000.0 * (sini - fc) - tfc * (Ep / 24.0)
                    self._ETA[cell] = Tb * (Ep / 24.0)
                elif Tb >= tsc and Tb < twp:
                    s = wp + (sc - wp) * (nu / (nu - nuw) * np.exp(-1 * ((nu - nuw) / (sc - wp)) * (Tb - tsc)) - nuw / (nu - nuw))
                    self._D[cell] = pc * ZR * 1000.0 * (sini - fc) - tfc * Ep / 24.0
                    self._ETA[cell] = 1000.0 * ZR * pc * (sini - s) - self._D[cell]
                else:
                    s = hgw + (wp - hgw) * np.exp(-1 * (nuw / (wp - hgw)) * max(Tb - twp, 0.0))
                    self._D[cell] = pc * ZR * 1000.0 * (sini - fc) - tfc * Ep / 24.0
                    self._ETA[cell] = 1000.0 * ZR * pc * (sini - s) - self._D[cell]
            elif sini < fc and sini >= sc:
                tfc = 0.0
                tsc = (sini - sc) / nu
                twp = (sc - wp) / (nu - nuw) * np.log(nu / nuw) + tsc
                if Tb < tsc:
                    s = sini - nu * Tb
                    self._D[cell] = 0.0
                    self._ETA[cell] = 1000.0 * ZR * pc * (sini - s)
                elif Tb >= tsc and Tb < twp:
                    s = wp + (sc - wp) * (nu / (nu - nuw) * np.exp(-1 * ((nu - nuw) / (sc - wp)) * (Tb - tsc)) - nuw / (nu - nuw))
                    self._D[cell] = 0
                    self._ETA[cell] = 1000.0 * ZR * pc * (sini - s)
                else:
                    s = hgw + (wp - hgw) * np.exp(-1 * (nuw / (wp - hgw)) * (Tb - twp))
                    self._D[cell] = 0.0
                    self._ETA[cell] = 1000.0 * ZR * pc * (sini - s)
            elif sini < sc and sini >= wp:
                tfc = 0
                tsc = 0
                twp = (sc - wp) / (nu - nuw) * np.log(1 + (nu - nuw) * (sini - wp) / (nuw * (sc - wp)))
                if Tb < twp:
                    s = wp + (sc - wp) / (nu - nuw) * (np.exp(-1 * ((nu - nuw) / (sc - wp)) * Tb) * (nuw + (nu - nuw) / (sc - wp) * (sini - wp)) - nuw)
                    self._D[cell] = 0.0
                    self._ETA[cell] = 1000.0 * ZR * pc * (sini - s)
                else:
                    s = hgw + (wp - hgw) * np.exp(-1 * (nuw / (wp - hgw)) * (Tb - twp))
                    self._D[cell] = 0.0
                    self._ETA[cell] = 1000.0 * ZR * pc * (sini - s)
            else:
                tfc = 0.0
                tsc = 0.0
                twp = 0.0
                s = hgw + (sini - hgw) * np.exp(-1 * (nuw / (wp - hgw)) * Tb)
                self._D[cell] = 0.0
                self._ETA[cell] = 1000.0 * ZR * pc * (sini - s)
            self._water_stress[cell] = min(max((sc - (s + sini) / 2.0) / (sc - wp), 0.0) ** 4.0, 1.0)
            self._S[cell] = s
            self._SO[cell] = s
            self._Sini[cell] = sini

        current_time += (Tb + Tr) / 8766.0
        return current_time