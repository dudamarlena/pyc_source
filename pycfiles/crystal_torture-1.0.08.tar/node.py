# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cor/bin/src/crystal_torture/crystal_torture/node.py
# Compiled at: 2018-08-07 03:23:00


class Node:
    """
    Node class
    """

    def __init__(self, index, element, labels, neighbours_ind, neighbours=None):
        """
        Initialise a Node.

        Args:
            - index (Int): node index
            - element (Str): element on node
            - labels(Dict(Str:Str)): dictionary of labels associated to the node.
            - neighbours_ind(set{int}): set of neighbour indices for the node in unit cell 
            - neighbours(set{Node}): set of neighbour Nodes for the node in unit cell
            - halo_neigh_ind(set{int}): set of neighbour indices for node in halo
            - halo_neigh(set{Node}): set of neighbour Nodes for this node in halo
        """
        self.index = index
        self.element = element
        self.labels = labels
        self.neighbours_ind = neighbours_ind
        self.neighbours = neighbours
        self.tortuosity = None
        self.dist = 0
        return