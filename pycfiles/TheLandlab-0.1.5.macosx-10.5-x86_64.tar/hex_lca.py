# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /anaconda/lib/python2.7/site-packages/landlab/components/cellular_automata/hex_lca.py
# Compiled at: 2014-09-23 12:37:24
"""
hex_lca.py: simple hexagonal Landlab cellular automaton

This file defines the HexLCA class, which is a sub-class of 
LandlabCellularAutomaton that implements a simple, non-oriented, hex-grid
CA. Like its parent class, HexLCA implements a continuous-time, stochastic,
pair-based CA. The hex grid has 3 principal directions, rather than 2 for a
raster. Hex grids are often used in CA models because of their symmetry.

Created GT Sep 2014
"""
from landlab_ca import LandlabCellularAutomaton, Transition
import landlab

class HexLCA(LandlabCellularAutomaton):

    def __init__(self, model_grid, node_state_dict, transition_list, initial_node_states):
        assert type(model_grid) is landlab.grid.hex.HexModelGrid, 'model_grid must be a Landlab HexModelGrid'
        self.number_of_orientations = 1
        super(HexLCA, self).__init__(model_grid, node_state_dict, transition_list, initial_node_states)


if __name__ == '__main__':
    mg = landlab.HexModelGrid(4, 3, 1.0)
    nsd = {0: 'yes', 1: 'no'}
    xnlist = []
    xnlist.append(Transition((0, 1, 0), (1, 1, 0), 1.0, 'hexxing'))
    nsg = mg.add_zeros('node', 'node_state_grid')
    hlca = HexLCA(mg, nsd, xnlist, nsg)
    print hlca.__dict__