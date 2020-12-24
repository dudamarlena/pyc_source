# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /anaconda/lib/python2.7/site-packages/landlab/components/cellular_automata/oriented_hex_lca.py
# Compiled at: 2014-09-23 12:37:24
"""
oriented_hex_lca.py: simple hexagonal Landlab cellular automaton

This file defines the OrientedHexLCA class, which is a sub-class of 
LandlabCellularAutomaton that implements a simple, non-oriented, hex-grid
CA. Like its parent class, OrientedHexLCA implements a continuous-time, stochastic,
pair-based CA. The hex grid has 3 principal directions, rather than 2 for a
raster. Hex grids are often used in CA models because of their symmetry.

Created GT Sep 2014
"""
from numpy import zeros
from landlab_ca import LandlabCellularAutomaton, Transition
import landlab

class OrientedHexLCA(LandlabCellularAutomaton):

    def __init__(self, model_grid, node_state_dict, transition_list, initial_node_states):
        assert type(model_grid) is landlab.grid.hex.HexModelGrid, 'model_grid must be a Landlab HexModelGrid'
        self.number_of_orientations = 3
        super(OrientedHexLCA, self).__init__(model_grid, node_state_dict, transition_list, initial_node_states)

    def setup_array_of_orientation_codes(self):
        """
        Creates and configures an array that contain the orientation code for 
        each active link (and corresponding cell pair).
        
        Parameters
        ----------
        (none)
        
        Returns
        -------
        (none)
        
        Creates
        -------
        self.active_link_orientation : 1D numpy array
        
        Notes
        -----
        This overrides the method of the same name in landlab_ca.py. If the hex
        grid is oriented such that one of the 3 axes is vertical (a 'vertical'
        grid), then the three orientations are:
            0 = vertical (0 degrees clockwise from vertical)
            1 = right and up (60 degrees clockwise from vertical)
            2 = right and down (120 degrees clockwise from vertical)
        If the grid is oriented with one principal axis horizontal ('horizontal'
        grid), then the orientations are:
            0 = up and left (30 degrees counter-clockwise from vertical)
            1 = up and right (30 degrees clockwise from vertical)
            2 = horizontal (90 degrees clockwise from vertical)
        """
        self.active_link_orientation = zeros(self.grid.number_of_active_links, dtype=int)
        for j in range(self.grid.number_of_active_links):
            i = self.grid.active_links[j]
            dy = self.grid.node_y[self.grid.link_tonode[i]] - self.grid.node_y[self.grid.link_fromnode[i]]
            dx = self.grid.node_x[self.grid.link_tonode[i]] - self.grid.node_x[self.grid.link_fromnode[i]]
            if dx <= 0.0:
                self.active_link_orientation[j] = 0
            elif dy <= 0.0:
                self.active_link_orientation[j] = 2
            elif dx > 0.0 and dy > 0.0:
                self.active_link_orientation[j] = 1
            elif not False:
                raise AssertionError('Non-handled link orientation case')


if __name__ == '__main__':
    print 'main here'
    from landlab import HexModelGrid
    mg = HexModelGrid(2, 3, 1.0, orientation='vertical', reorient_links=True)
    print mg.number_of_active_links
    nsd = {0: 'yes', 1: 'no'}
    xnlist = []
    xnlist.append(Transition((0, 1, 0), (1, 0, 0), 1.0, 'falling'))
    nsg = mg.add_zeros('node', 'node_state_grid')
    ohlca = OrientedHexLCA(mg, nsd, xnlist, nsg)
    for i in range(mg.number_of_active_links):
        j = mg.active_links[i]
        print i, j, '(', mg.node_x[mg.link_fromnode[j]], ',', mg.node_y[mg.link_fromnode[j]],
        print ')', '(', mg.node_x[mg.link_tonode[j]], ',', mg.node_y[mg.link_tonode[j]],
        print ')', ohlca.active_link_orientation[i]