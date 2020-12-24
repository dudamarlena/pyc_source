# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/apgl/generator/StochasticKroneckerGenerator.py
# Compiled at: 2010-11-21 16:07:56
import numpy
from apgl.util.Parameter import Parameter
from apgl.graph.VertexList import VertexList
from apgl.graph.SparseGraph import SparseGraph

class StochasticKroneckerGenerator(object):
    """
    A class which generates graphs according to the Stochastic Kronecker method.
    """

    def __init__(self, initialGraph, k):
        """
        Initialise with a starting graph, and number of iterations k. The weights
        of the initial graph correspond to probabilities. 

        :param initialGraph: The intial graph to use.
        :type initialGraph: :class:`apgl.graph.AbstractMatrixGraph`

        :param k: The number of iterations.
        :type k: :class:`int`
        """
        Parameter.checkInt(k, 1, float('inf'))
        edgeVals = initialGraph.getEdgeValues(initialGraph.getAllEdges())
        Parameter.checkList(edgeVals, Parameter.checkFloat, [0.0, 1.0])
        W = initialGraph.getWeightMatrix()
        if (numpy.diag(W) == numpy.zeros(W.shape[0])).any():
            raise ValueError('Initial graph must have all self-edges')
        self.initialGraph = initialGraph
        self.k = k

    def setK(self, k):
        """
        Set the number of iterations k.

        :param initialGraph: The number of iterations.
        :type initialGraph: :class:`int`
        """
        Parameter.checkInt(k, 1, float('inf'))
        self.k = k

    def generateGraph(self):
        """
        Generate a Kronecker graph
        """
        W = self.initialGraph.getWeightMatrix()
        Wi = W
        for i in range(1, self.k):
            Wi = numpy.kron(Wi, W)

        P = numpy.random.rand(Wi.shape[0], Wi.shape[0])
        Wi = numpy.array(P < Wi, numpy.float64)
        vList = VertexList(Wi.shape[0], 0)
        graph = SparseGraph(vList, self.initialGraph.isUndirected())
        graph.setWeightMatrix(Wi)
        return graph