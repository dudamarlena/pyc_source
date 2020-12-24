# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /anaconda/lib/python2.7/site-packages/landlab/components/dem_support/dem_boundary_conditions.py
# Compiled at: 2014-10-01 12:52:58
"""

Classes for Landlab that deal with setting boundary conditions if running
on a DEM.  This takes advantage of methods in the grid, but combines them
to make it easier for a user.

Last updated NG 8/2013

"""
from landlab import RasterModelGrid
import numpy as np, pylab

class WatershedBoundaryConditions(object):
    """
    If using a DEM of a watershed, this class will properly 
    set the boundary conditions.
    """

    def __init__(self):
        """
        what does this need?
        """
        pass

    def set_bc_node_coords(self, mg, node_data, nodata_value, outlet_row, outlet_column):
        """
        Sets the boundary conditions for a watershed.
        Assumes that outlet is already known.
        
        This must be passed the grid, node_data and nodata_value, 
        and the values of the outlet_row and outlet_column.
        """
        mg.set_nodata_nodes_to_inactive(node_data, nodata_value)
        outlet_node = mg.grid_coords_to_node_id(outlet_row, outlet_column)
        mg.set_fixed_value_boundaries(outlet_node)

    def set_bc_node_id(self, mg, node_data, nodata_value, outlet_node):
        """
        Sets the boundary conditions for a watershed.
        Assumes that outlet is already known.
        
        This must be passed the grid, node_data and nodata_value, 
        and the id of the outlet node.
        """
        mg.set_nodata_nodes_to_inactive(node_data, nodata_value)
        mg.set_fixed_value_boundaries(outlet_node)

    def set_bc_find_outlet(self, mg, node_data, nodata_value):
        """
        Finds the node adjacent to a boundary node with the smallest value.
        This node is set as the outlet.
        
        This must be passed the grid, node_data and nodata_value.
        """
        mg.set_inactive_boundaries(True, True, True, True)
        mg.set_nodata_nodes_to_inactive(node_data, nodata_value)
        if min(node_data) == nodata_value:
            locs = list(np.where(node_data > nodata_value)[0])
            min_val = np.min(node_data[locs])
            min_locs = list(np.where(node_data == min_val)[0])
            not_found = True
            while not_found:
                local_not_found = True
                i = 0
                while i < len(min_locs) and local_not_found:
                    if mg.has_boundary_neighbor(min_locs[i]):
                        local_not_found = False
                        outlet_loc = min_locs[i]
                    else:
                        i += 1

                if local_not_found:
                    locs = list(np.where(node_data > min_val)[0])
                    min_val = np.min(node_data[locs])
                    min_locs = list(np.where(node_data == min_val)[0])
                else:
                    not_found = False

        else:
            min_val = np.min(node_data)
            if min_val == nodata_value:
                locs = list(np.where(node_data > nodata_value)[0])
                min_val = np.min(node_data[locs])
            min_locs = list(np.where(node_data == min_val)[0])
            not_found = True
            while not_found:
                local_not_found = True
                i = 0
                while i < len(min_locs) and local_not_found:
                    if mg.has_boundary_neighbor(min_locs[i]):
                        local_not_found = False
                        outlet_loc = min_locs[i]
                    else:
                        i += 1

                if local_not_found:
                    locs = list(np.where(node_data > min_val)[0])
                    min_val = np.min(node_data[locs])
                    if min_val == nodata_value:
                        locs = list(np.where(node_data > nodata_value)[0])
                        min_val = np.min(node_data[locs])
                    min_locs = list(np.where(node_data == min_val)[0])
                else:
                    not_found = False

        mg.set_fixed_value_boundaries(outlet_loc)
        return outlet_loc