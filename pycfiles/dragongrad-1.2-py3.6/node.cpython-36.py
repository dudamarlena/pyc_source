# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/autograd/node.py
# Compiled at: 2018-12-12 06:22:23
# Size of source mod 2**32: 5365 bytes
import autograd as ad, numpy as np
from autograd import config

class C_graph:
    __doc__ = '\n    aggregating class for the nodes in the computational graph\n    '

    def __init__(self, nodes=[]):
        self.ids = []
        self.input_node = []
        self.output_node = None
        self.input_shapes = []

    def reset_graph(self):
        for node in config.list_of_nodes:
            node.gradient = None
            node.times_visited = 0
            node.times_used = 0

    def define_path(self, node):
        """
        make a first backward pass without doing any computation
        It is just meant to check which variables are involved in the computation of the node given
        """
        if node.childrens != []:
            for child in node.childrens:
                node_child = child['node']
                node_child.times_used += 1
                self.define_path(node_child)

        for node in self.input_node:
            if node.times_used == 0:
                node.gradient = np.zeros((node.output_dim, self.output_node.output_dim))


class Node:
    __doc__ = '\n    basic element of the computational graph\n    '

    def __init__(self, output_dim=None):
        if ad.c_graph.ids == []:
            self.id = 0
            ad.c_graph.ids += [0]
        else:
            self.id = ad.c_graph.ids[(-1)] + 1
            ad.c_graph.ids += [self.id]
        self.output_dim = output_dim
        self.times_used = 0
        self.times_visited = 0
        self.gradient = None
        self.childrens = []

    def backward(self):
        """
        implement reverse AD, return the gradient of current variable w.r. input Variables
        input variables are the ones who don't have any childrens
        """
        if self.gradient is None:
            self.gradient = np.eye(self.output_dim)
            self.times_visited += 1
            if self.childrens == []:
                return self.gradient
            self.backward()
        elif self.childrens != []:
            for child in self.childrens:
                node, jacobian = child['node'], child['jacobian']
                new_grad = np.dot(self.gradient, jacobian)
                if node.gradient is None:
                    node.gradient = new_grad
                else:
                    node.gradient += new_grad
                node.times_visited += 1
                if node.times_used == node.times_visited:
                    node.backward()
                    continue