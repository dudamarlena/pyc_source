# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /anaconda/lib/python2.7/site-packages/landlab/components/cellular_automata/boundaries/hex_lattice_tectonicizer.py
# Compiled at: 2015-02-11 19:25:27
"""
hex_lattice_tectonicizer.py

Models discrete normal-fault offset on a 2D hex lattice with a rectangular
shape and with one orientation of the nodes being vertical.

The intention here is to use a particle (LCA) model to represent the evolution
of a 2D hillslope, with the hex_lattice_tectonicizer serving to shift the nodes
either upward (simple vertical uplift relative to baselevel), or up and
sideways (representing motion on a fault plane).

Created on Mon Nov 17 08:01:49 2014

@author: gtucker
"""
from landlab import HexModelGrid
from numpy import amax, zeros, arange
from pylab import figure
_DEFAULT_NUM_ROWS = 20
_DEFAULT_NUM_COLS = 15
_TAN60 = 1.732

class HexLatticeTectonicizer(object):
    """Base class from which classes to represent particular baselevel/fault
    geometries are derived.
    """

    def __init__(self, grid=None, node_state=None):
        if grid is None:
            num_rows = _DEFAULT_NUM_ROWS
            num_cols = _DEFAULT_NUM_COLS
            self.grid = HexModelGrid(num_rows, num_cols, dx=1.0, orientation='vertical', shape='rect', reorient_links=True)
        else:
            assert grid.orientation == 'vertical', 'Grid must have vertical orientation'
            self.grid = grid
        if node_state is None:
            self.node_state = self.grid.add_zeros('node', 'node_state_map')
        else:
            print 'setting node state'
            self.node_state = node_state
        self.nr = self.grid.number_of_node_rows
        self.nc = self.grid.number_of_node_columns
        return


class LatticeNormalFault(HexLatticeTectonicizer):
    """Represents a 60 degree, left-dipping normal fault, and handles discrete
    offsets for a hex grid that has vertical columns and a rectangular shape.
    """

    def __init__(self, fault_x_intercept=0.0, grid=None, node_state=None):
        super(LatticeNormalFault, self).__init__(grid, node_state)
        assert fault_x_intercept < amax(self.grid.node_x) - 0.57735
        in_footwall = self.grid.node_y < _TAN60 * (self.grid.node_x - fault_x_intercept)
        self.first_fw_col = 0
        n = 0
        while not in_footwall[n]:
            n += self.nr
            self.first_fw_col += 1

        self.num_fw_rows = zeros(self.nc)
        for c in range(self.nc):
            current_row = 0
            while current_row < self.nr and in_footwall[(current_row + c * self.nr)]:
                self.num_fw_rows[c] += 1
                current_row += 1

    def do_offset(self, rock_state=1):
        """Applies 60-degree normal-fault offset to a hexagonal grid with
        vertical node orientation and rectangular arrangement of nodes.
        """
        for c in range(self.grid.number_of_node_columns - 1, self.first_fw_col - 1, -1):
            row_offset = 2 - c % 2
            n_base_nodes = min(self.num_fw_rows[c], row_offset)
            bottom_node = c * self.grid.number_of_node_rows
            self.node_state[bottom_node:(bottom_node + n_base_nodes)] = rock_state
            indices = arange(n_base_nodes, self.num_fw_rows[c], dtype=int) + bottom_node
            if len(indices) > 0:
                self.node_state[indices] = self.node_state[(indices - (self.nr + row_offset))]

        if self.first_fw_col == 0:
            self.node_state[:(self.n_footwall_rows[0])] = rock_state


class LatticeUplifter(HexLatticeTectonicizer):
    """Handles vertical uplift of interior (not edges) for a hexagonal lattice
    with vertical node orientation and rectangular node arrangement.
    """

    def __init__(self, grid=None, node_state=None):
        super(LatticeUplifter, self).__init__(grid, node_state)
        self.base_row_nodes = arange(self.nr, self.nr * (self.nc - 1), self.nr)

    def uplift_interior_nodes(self, rock_state=1):
        print 'in uin, ns is'
        print self.node_state
        for r in range(self.nr - 1, 0, -1):
            self.node_state[self.base_row_nodes + r] = self.node_state[(self.base_row_nodes + (r - 1))]

        self.node_state[self.base_row_nodes] = rock_state


def main():
    lnf = LatticeNormalFault()
    for i in range(13):
        lnf.do_offset()

    lnf.grid.hexplot(lnf.node_state)
    lu = LatticeUplifter()
    lu.uplift_interior_nodes()
    figure(2)
    for i in range(5):
        lu.uplift_interior_nodes()
        lu.grid.hexplot(lu.node_state)


if __name__ == '__main__':
    main()