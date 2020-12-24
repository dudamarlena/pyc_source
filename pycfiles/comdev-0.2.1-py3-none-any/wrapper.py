# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Python27\Lib\site-packages\comdet\wrapper.py
# Compiled at: 2014-08-01 01:42:59


class Node:
    sno = 0
    node_name = ''
    elems = []

    def __init__(self):
        self.elems = []

    def add_elem(self, elem):
        self.elems.append(elem)

    def no_of_elems(self):
        return len(self.elems)

    def display_elems(self):
        for e in self.elems:
            print '\t\t%s' % e


class Pool:
    nodes = {}

    def __init__(self):
        self.nodes = {}

    def add_node(self, node):
        n = Node()
        n.node_name = node
        self.nodes[node] = n
        return n

    def get_node(self, node):
        if node in self.nodes:
            return self.nodes[node]
        else:
            return

    def no_of_nodes(self):
        return len(self.nodes.keys())

    def display_node(self):
        for n in self.nodes.values():
            print n.node_name
            n.display_elems()