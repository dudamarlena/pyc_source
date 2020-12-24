# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /anaconda/lib/python2.7/site-packages/landlab/components/flow_accum/flow_accumulation2.py
# Compiled at: 2015-02-11 19:25:27
"""
    A python flow accumulation module. It is designed to be general, and to operate across multiple grids and multiple flow direction patterns. However, at the moment, only a steepest descent (single path) routing scheme is implemented.
    
    There remain some outstanding issues with the handling of boundary cells, which this component has inherited from flow_routing_D8.
    
    Created DEJH, 8/2013
"""
import landlab
from landlab import ModelParameterDictionary
import numpy as np

class AccumFlow(object):
    """
    This class allows the routing of flow around a landscape according to a previously calculated flow direction vector. It is not sensitive to grid type. It will eventually be able to work with discharges which are split across more than one node, but at the moment, assumes a single line of descent for a given node.
    """

    def __init__(self, grid):
        self.initialize(grid)

    def initialize(self, grid):
        self.grid = grid
        self.flow_accum_by_area = np.zeros(grid.number_of_nodes + 1)

    def calc_flowacc(self, grid, z, flowdirs):
        active_cell_ids = grid.get_active_cell_node_ids()
        try:
            height_order_active_cells = np.argsort(z[active_cell_ids])[::-1]
        except:
            print 'Cells could not be sorted by elevation. Does the data object contain the elevation vector?'

        try:
            sorted_flowdirs = flowdirs[active_cell_ids][height_order_active_cells]
        except:
            print 'Flow directions could not be sorted by elevation. Does the data object contain the flow direction vector?'

        self.flow_accum_by_area[active_cell_ids] = grid.cell_areas
        for i in xrange(len(sorted_flowdirs)):
            iter_height_order = height_order_active_cells[i]
            iter_sorted_fldirs = sorted_flowdirs[i]
            self.flow_accum_by_area[iter_sorted_fldirs] += self.flow_accum_by_area[active_cell_ids][iter_height_order]

        return self.flow_accum_by_area[:-1]