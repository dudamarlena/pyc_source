# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /anaconda/lib/python2.7/site-packages/landlab/components/vegetation_ca/CA_Veg_new.py
# Compiled at: 2015-03-08 15:33:09
from landlab import Component
import numpy as np
_VALID_METHODS = set(['Grid'])
GRASS = 0
SHRUB = 1
TREE = 2
BARE = 3
SHRUBSEEDLING = 4
TREESEEDLING = 5

def assert_method_is_valid(method):
    if method not in _VALID_METHODS:
        raise ValueError('%s: Invalid method name' % method)


class VegCA(Component):
    """1D and 2D vegetation dynamics.

    Landlab component that implements 1D and 2D vegetation dynamics model.
    """
    _name = 'VegCA'
    _input_var_names = set([
     'CumulativeWaterStress',
     'VegetationType'])
    _output_var_names = set([
     'PlantLiveIndex',
     'PlantAge'])
    _var_units = {'CumulativeWaterStress': 'Pa', 
       'VegetationType': 'None', 
       'PlantLiveIndex': 'Pa', 
       'PlantAge': 'Years'}

    def __init__(self, grid, data, **kwds):
        self._method = kwds.pop('method', 'Grid')
        self._Pemaxg = kwds.pop('Pemaxg', data['Pemaxg'])
        self._Pemaxsh = kwds.pop('Pemaxsh', data['Pemaxsh'])
        self._Pemaxtr = kwds.pop('Pemaxtr', data['Pemaxtr'])
        self._INg = kwds.pop('ING', data['ING'])
        self._th_g = kwds.pop('ThetaGrass', data['ThetaGrass'])
        self._th_sh = kwds.pop('ThetaShrub', data['ThetaShrub'])
        self._th_tr = kwds.pop('ThetaTree', data['ThetaTree'])
        self._th_sh_s = kwds.pop('ThetaShrubSeedling', data['ThetaShrubSeedling'])
        self._th_tr_s = kwds.pop('ThetaTreeSeedling', data['ThetaTreeSeedling'])
        self._Pmb_g = kwds.pop('PmbGrass', data['PmbGrass'])
        self._Pmb_sh = kwds.pop('PmbShrub', data['PmbShrub'])
        self._Pmb_tr = kwds.pop('PmbTree', data['PmbTree'])
        self._Pmb_sh_s = kwds.pop('PmbShrubSeedling', data['PmbShrubSeedling'])
        self._Pmb_tr_s = kwds.pop('PmbTreeSeedling', data['PmbTreeSeedling'])
        self._tpmax_sh = kwds.pop('tpmaxShrub', data['tpmaxShrub'])
        self._tpmax_tr = kwds.pop('tpmaxTree', data['tpmaxTree'])
        self._tpmax_sh_s = kwds.pop('tpmaxShrubSeedling', data['tpmaxShrubSeedling'])
        self._tpmax_tr_s = kwds.pop('tpmaxTreeSeedling', data['tpmaxTreeSeedling'])
        assert_method_is_valid(self._method)
        super(VegCA, self).__init__(grid, **kwds)
        for name in self._input_var_names:
            if name not in self.grid.at_cell:
                self.grid.add_zeros('cell', name, units=self._var_units[name])

        for name in self._output_var_names:
            if name not in self.grid.at_cell:
                self.grid.add_zeros('cell', name, units=self._var_units[name])

        self._cell_values = self.grid['cell']
        if np.where(grid['cell']['VegetationType'] != 0)[0].shape[0] == 0:
            grid['cell']['VegetationType'] = np.random.randint(0, 6, grid.number_of_cells)
        VegType = grid['cell']['VegetationType']
        tp = np.zeros(grid.number_of_cells, dtype=int)
        tp[VegType == TREE] = np.random.randint(0, self._tpmax_tr, np.where(VegType == TREE)[0].shape)
        tp[VegType == SHRUB] = np.random.randint(0, self._tpmax_sh, np.where(VegType == SHRUB)[0].shape)
        tp[VegType == TREESEEDLING] = np.random.randint(0, self._tpmax_tr_s, np.where(VegType == TREESEEDLING)[0].shape)
        tp[VegType == SHRUBSEEDLING] = np.random.randint(0, self._tpmax_sh_s, np.where(VegType == SHRUBSEEDLING)[0].shape)
        grid['cell']['PlantAge'] = tp

    def update(self, Edit_VegCov=True, time_elapsed=1):
        self._VegType = self._cell_values['VegetationType']
        self._CumWS = self._cell_values['CumulativeWaterStress']
        self._live_index = self._cell_values['PlantLiveIndex']
        self._tp = self._cell_values['PlantAge'] + time_elapsed
        shrub_seedlings = np.where(self._VegType == SHRUBSEEDLING)[0]
        tree_seedlings = np.where(self._VegType == TREESEEDLING)[0]
        matured_shrubs = np.where(self._tp[shrub_seedlings] > self._tpmax_sh_s)[0]
        matured_trees = np.where(self._tp[tree_seedlings] > self._tpmax_tr_s)[0]
        self._VegType[shrub_seedlings[matured_shrubs]] = SHRUB
        self._VegType[tree_seedlings[matured_trees]] = TREE
        self._tp[shrub_seedlings[matured_shrubs]] = 0
        self._tp[tree_seedlings[matured_trees]] = 0
        self._live_index = 1 - self._CumWS
        bare_cells = np.where(self._VegType == BARE)[0]
        n_bare = len(bare_cells)
        first_ring = self.grid.get_looped_cell_neighbor_list(bare_cells)
        second_ring = self.grid.get_second_ring_looped_cell_neighbor_list(bare_cells)
        veg_type_fr = self._VegType[first_ring]
        veg_type_sr = self._VegType[second_ring]
        Sh_WS_fr = WS_PFT(veg_type_fr, SHRUB, self._live_index[first_ring])
        Tr_WS_fr = WS_PFT(veg_type_fr, TREE, self._live_index[first_ring])
        Tr_WS_sr = WS_PFT(veg_type_sr, TREE, self._live_index[second_ring])
        n = count(veg_type_fr, SHRUB)
        Phi_sh = Sh_WS_fr / 8.0
        Phi_tr = (Tr_WS_fr + Tr_WS_sr / 2.0) / 8.0
        Phi_g = np.mean(self._live_index[np.where(self._VegType == GRASS)])
        Pemaxg = self._Pemaxg * np.ones(n_bare)
        Pemaxsh = self._Pemaxsh * np.ones(n_bare)
        Pemaxtr = self._Pemaxtr * np.ones(n_bare)
        Peg = np.amin(np.vstack((Phi_g / (n * self._INg), Pemaxg)), axis=0)
        Pesh = np.amin(np.vstack((Phi_sh, Pemaxsh)), axis=0)
        Petr = np.amin(np.vstack((Phi_tr, Pemaxtr)), axis=0)
        Select_PFT_E = np.random.choice([GRASS, SHRUBSEEDLING, TREESEEDLING], n_bare)
        Pest = np.choose(Select_PFT_E, [Peg, 0, 0, 0, Pesh, Petr])
        R_Est = np.random.rand(n_bare)
        Establish = np.int32(np.where(np.greater_equal(Pest, R_Est) == True)[0])
        self._VegType[bare_cells[Establish]] = Select_PFT_E[Establish]
        self._tp[bare_cells[Establish]] = 0
        plant_cells = np.where(self._VegType != BARE)[0]
        n_plant = len(plant_cells)
        Theta = np.choose(self._VegType[plant_cells], [
         self._th_g, self._th_sh, self._th_tr,
         0, self._th_sh_s, self._th_tr_s])
        PMd = self._CumWS[plant_cells] - Theta
        PMd[PMd < 0.0] = 0.0
        tpmax = np.choose(self._VegType[plant_cells], [
         200000, self._tpmax_sh, self._tpmax_tr,
         0, self._tpmax_sh_s, self._tpmax_tr_s])
        PMa = np.zeros(n_plant)
        tp_plant = self._tp[plant_cells]
        tp_greater = np.where(tp_plant > 0.5 * tpmax)[0]
        PMa[tp_greater] = (tp_plant[tp_greater] - 0.5 * tpmax[tp_greater]) / (0.5 * tpmax[tp_greater]) - 1
        PMb = np.choose(self._VegType[plant_cells], [
         self._Pmb_g, self._Pmb_sh, self._Pmb_tr, 0,
         self._Pmb_sh_s, self._Pmb_tr_s])
        PM = PMd + PMa + PMb
        PM[PM > 1.0] = 1.0
        R_Mor = np.random.rand(n_plant)
        Mortality = np.int32(np.where(np.greater_equal(PM, R_Mor) == True)[0])
        self._VegType[plant_cells[Mortality]] = BARE
        self._tp[plant_cells[Mortality]] = 0
        self._cell_values['PlantAge'] = self._tp
        if Edit_VegCov:
            self.grid['cell']['VegetationCover'] = np.zeros(self.grid.number_of_cells)
            self.grid['cell']['VegetationCover'][self._VegType != BARE] = 1.0
        self._bare_cells = bare_cells
        self._Established = bare_cells[Establish]
        self._plant_cells = plant_cells
        self._Mortified = plant_cells[Mortality]


def count(Arr, value):
    Res = np.zeros(Arr.shape[0], dtype=int)
    x, y = Arr.shape
    for i in range(0, x):
        for j in range(0, y):
            if Arr[i][j] == value:
                Res[i] += 1

    return Res


def WS_PFT(VegType, PlantType, WS):
    Phi = np.zeros(WS.shape[0])
    x, y = WS.shape
    for i in range(0, x):
        for j in range(0, y):
            if VegType[i][j] == PlantType:
                Phi[i] += WS[i][j]

    return Phi