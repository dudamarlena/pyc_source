# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /anaconda/lib/python2.7/site-packages/landlab/components/flow_routing/flow_routing_D8.py
# Compiled at: 2015-02-11 19:25:27
"""

Python implementation of d8 routing scheme for
Landlab with a rectangular, uniform, mesh.

Some issues that might come up ...
This class relies on a method in model_grid called
find_node_in_direction_of_max_slope.  That method does not do
any boundary checking.  It needs to be done somewhere, maybe here,
maybe there?  Alternatively, if boundary elevations are always set
in a consistent way depending on the type of bounary, maybe no boundary
checking is needed?

Last updated NG 8/2013

"""
from numpy import *

class RouteFlowD8(object):
    """
    This class finds the steepest path among 8 possible directions, so
    diagonals are considered.
    The class assumes that the model is using a rectangular, uniform (raster)
    grid.
    """

    def __init__(self, num_nodes):
        """
        This sets the num_cells parameter.
        This class assumes that the number of cells does not change after a 
        class item has been instantiated.
        """
        self.num_nodes = num_nodes
        self.initialize()

    def initialize(self):
        """
        This sets up the flow direction vector.
        It is initialized to -1 for all nodes.
        A -1 flowdirs value indicates a boundary node.
        """
        self.flowdirs = -ones(self.num_nodes, dtype=int)

    def calc_flowdirs(self, mg, z):
        """
        This assigns the flow directions using the function
        find_node_in_direction_of_max_slope in the model_grid.
        The flowdirs vector contains the node id that a node flows to. 
        If the node is a boundary node, the flowdirs vector has a value of -1.
        
        This now only applies to interior nodes.
        However, should a fixed value node, which counts as an interior node,
        have a flow direction?  Still not sure about this.
        
        Method inputs: the model grid and elevation vector 
        Method returns: the flow direction vector, and as of DEJH modifications
        Sept 2013, the maximum (most steeply downhill) slope leaving each node.
        """
        self.gradients_on_active_links = mg.calculate_gradients_at_active_links(z)
        max_slopes, self.flowdirs = mg.calculate_steepest_descent_on_nodes(z, self.gradients_on_active_links, dstr_node_ids=self.flowdirs)
        return (
         self.flowdirs, max_slopes)