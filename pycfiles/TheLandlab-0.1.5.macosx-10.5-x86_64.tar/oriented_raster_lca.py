# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /anaconda/lib/python2.7/site-packages/landlab/components/cellular_automata/oriented_raster_lca.py
# Compiled at: 2015-02-11 19:25:27
"""
oriented_raster_lca.py: simple raster Landlab cellular automaton, with 
cell-pair transitions that depend on orientation (vertical or horizontal)

This file defines the OrientedRasterLCA class, which is a sub-class of 
LandlabCellularAutomaton that implements a simple, oriented, raster-grid
CA. Like its parent class, OrientedRasterLCA implements a continuous-time, 
stochastic, pair-based CA.

Created GT Sep 2014
"""
from numpy import zeros
from landlab_ca import LandlabCellularAutomaton, Transition
import landlab
_DEBUG = False

class OrientedRasterLCA(LandlabCellularAutomaton):

    def __init__(self, model_grid, node_state_dict, transition_list, initial_node_states):
        if _DEBUG:
            print 'OrientedRasterLCA.__init__ here'
        assert type(model_grid) is landlab.grid.raster.RasterModelGrid, 'model_grid must be a Landlab RasterModelGrid'
        self.number_of_orientations = 2
        super(OrientedRasterLCA, self).__init__(model_grid, node_state_dict, transition_list, initial_node_states)
        if _DEBUG:
            print 'ORLCA:'
            print self.n_xn
            print self.xn_to
            print self.xn_rate

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
        This overrides the method of the same name in landlab_ca.py.
        """
        self.active_link_orientation = zeros(self.grid.number_of_active_links, dtype=int)
        dy = self.grid.node_y[self.grid.link_tonode[self.grid.active_links]] - self.grid.node_y[self.grid.link_fromnode[self.grid.active_links]]
        self.active_link_orientation = dy.astype(int)
        if _DEBUG:
            print self.active_link_orientation


if __name__ == '__main__':
    mg = landlab.RasterModelGrid(3, 4, 1.0)
    nsd = {0: 'yes', 1: 'no'}
    xnlist = []
    xnlist.append(Transition((0, 1, 0), (1, 1, 0), 1.0, 'frogging'))
    nsg = mg.add_zeros('node', 'node_state_grid')
    orlca = OrientedRasterLCA(mg, nsd, xnlist, nsg)
    print orlca.__dict__