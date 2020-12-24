# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /anaconda/lib/python2.7/site-packages/landlab/grid/grid_funcs.py
# Compiled at: 2014-09-23 12:37:24
import numpy as np

def resolve_values_on_active_links(grid, active_link_values, out=None):
    """
    Takes a set of values defined on active links, and returns those values
    resolved into the x and y directions.
    Two link arrays are returned; x, then y.
    """
    if out is None:
        out = grid.empty(centering='active_link')
    return (
     np.multiply((grid.node_x[grid.activelink_tonode] - grid.node_x[grid.activelink_fromnode]) / grid.active_link_length, active_link_values, out=out),
     np.multiply((grid.node_y[grid.activelink_tonode] - grid.node_y[grid.activelink_fromnode]) / grid.active_link_length, active_link_values, out=out))


def resolve_values_on_links(grid, link_values, out=None):
    """
    Takes a set of values defined on active links, and returns those values
    resolved into the x and y directions.
    Two link arrays are returned; x, then y.
    """
    if out is None:
        out = grid.empty(centering='link')
    return (
     np.multiply((grid.node_x[grid.link_tonode] - grid.node_x[grid.link_fromnode]) / grid.link_length, link_values, out=out),
     np.multiply((grid.node_y[grid.link_tonode] - grid.node_y[grid.link_fromnode]) / grid.link_length, link_values, out=out))


def calculate_gradients_at_active_links(grid, node_values, out=None):
    """
    Calculates the gradient in *quantity* node_values at each active link in
    the grid.
    Convention is POSITIVE UP.
    """
    if out is None:
        out = grid.empty(centering='active_link')
    return np.divide(node_values[grid.activelink_tonode] - node_values[grid.activelink_fromnode], grid.link_length[grid.active_links], out=out)


def calculate_gradients_at_links(grid, node_values, out=None):
    """
    Calculates the gradient in *quantity* node_values at each link in
    the grid.
    Convention is POSITIVE UP.
    """
    if out is None:
        out = grid.empty(centering='link')
    return np.divide(node_values[grid.link_tonode] - node_values[grid.link_fromnode], grid.link_length, out=out)


def calculate_diff_at_active_links(grid, node_values, out=None):
    """
    Calculates the difference in quantity *node_values* at each active link
    in the grid.
    Slope UP is positive.
    """
    if out is None:
        out = grid.empty(centering='active_link')
    return np.subtract(node_values[grid.activelink_tonode], node_values[grid.activelink_fromnode], out=out)


def calculate_diff_at_links(grid, node_values, out=None):
    """
    Calculates the difference in quantity *node_values* at each link in the
    grid.
    Slope UP is positive.
    """
    if out is None:
        out = grid.empty(centering='link')
    return np.subtract(node_values[grid.link_tonode], node_values[grid.link_fromnode], out=out)


def calculate_flux_divergence_at_nodes(grid, active_link_flux, out=None):
    """
    Same as calculate_flux_divergence_at_active_cells, but works with and
    returns a list of net unit fluxes that corresponds to all nodes, rather
    than just active cells. 
    
    Note that we don't compute net unit fluxes at
    boundary nodes (which don't have active cells associated with them, and 
    often don't have cells of any kind, because they are on the perimeter), 
    but simply return zeros for these entries. The advantage is that the 
    caller can work with node-based arrays instead of active-cell-based 
    arrays.
    """
    assert len(active_link_flux) == grid.number_of_active_links, 'incorrect length of active_link_flux array'
    if out is None:
        out = grid.empty(centering='node')
    out.fill(0.0)
    net_unit_flux = out
    assert len(net_unit_flux) == grid.number_of_nodes
    flux = np.zeros(len(active_link_flux) + 1)
    flux[:(len(active_link_flux))] = active_link_flux * grid.face_width
    for i in xrange(np.size(grid.node_active_inlink_matrix, 0)):
        net_unit_flux += flux[grid.node_active_outlink_matrix[i][:]]
        net_unit_flux -= flux[grid.node_active_inlink_matrix[i][:]]

    net_unit_flux[grid.activecell_node] /= grid.active_cell_areas
    return net_unit_flux