# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/cor/bin/src/crystal_torture/crystal_torture/node.py
# Compiled at: 2018-05-30 10:29:45
# Size of source mod 2**32: 919 bytes


class Node:
    """Node"""

    def __init__(self, index, element, labels, neighbours_ind, neighbours=None):
        """
        Initialise a Node.

        Args:
            index (Int): node index
            element (Str): element on node
            labels(Dict(Int:Str)): dictionary of labels associated to the node.
            neighbours_ind(set{int}): set of neighbour indices for the node in unit cell 
            neighbours(set{Node}): set of neighbour Nodes for the node in unit cell
            halo_neigh_ind(set{int}): set of neighbour indices for node in halo
            halo_neigh(set{Node}): set of neighbour Nodes for this node in halo
        """
        self.index = index
        self.element = element
        self.labels = labels
        self.neighbours_ind = neighbours_ind
        self.neighbours = neighbours
        self.tortuosity = None
        self.dist = 0