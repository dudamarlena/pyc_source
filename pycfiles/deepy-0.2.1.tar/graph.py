# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/shu/research/deepy/deepy/networks/graph.py
# Compiled at: 2016-04-20 00:05:45
from . import NeuralNetwork

class ComputationalGraph(NeuralNetwork):
    """
    A class for defining computational graphs.
    This class can be used to design very complex models, such as Neural Turing Machine.
    """

    def __init__(self, input_dim=0, model=None, input_tensor=None, cost=None, output=None, blocks=None, input_vars=None, target_vars=None):
        """
        Create a basic network.

        Parameters:
            input_dim - dimension of input variable
            model - a short hand to specify the model
            config - network configuration
            input_tensor - specify the tensor of input if it's special
        """
        super(ComputationalGraph, self).__init__(input_dim, input_tensor=input_tensor)
        if model:
            self.stack(model)
        if output:
            self.stack(output)
        if cost:
            self.stack(cost)
        if blocks:
            self.register(*blocks)
        if input_vars:
            self.input_variables = [ t.tensor for t in input_vars ]
        if target_vars:
            self.target_variables = [ t.tensor for t in target_vars ]

    @property
    def cost(self):
        return self.output

    @property
    def test_cost(self):
        return self.test_output