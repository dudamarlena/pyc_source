# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/apgl/generator/SmallWorldGenerator.py
# Compiled at: 2011-05-07 11:23:24
from apgl.graph.AbstractMatrixGraph import AbstractMatrixGraph
from apgl.generator.AbstractGraphGenerator import AbstractGraphGenerator
from apgl.util.Parameter import Parameter
import numpy

class SmallWorldGenerator(AbstractGraphGenerator):
    """
    Generates a random graph using the Small World Model proposed by Watts and
    Strogatz. We start with a regular lattice and rewire nodes according to some
    probability p. Only works with undirected graphs currently.
    """

    def __init__(self, p, k):
        """
        Create a small-world generator with k initial neighbours and a re-wiring probability p

        :param p: the probability of rewiring an edge.
        :type p: :class:`float`

        :param k: the number of neighbours in the regular lattice.
        :type k: :class:`int`

        :param edgeWeight: the non-zero weight of newly created edges.
        :type edgeWeight: :class:`float`
        """
        self.setP(p)
        self.setK(k)

    def setP(self, p):
        """
        Set the rewiring probability.

        :param p: the probability of rewiring an edge.
        :type p: :class:`float`
        """
        Parameter.checkFloat(p, 0.0, 1.0)
        self.p = p

    def setK(self, k):
        """
        The number of neighbours of each vertex.

        :param k: the number of neighbours in the regular lattice.
        :type k: :class:`int`
        """
        Parameter.checkIndex(k, 0, float('inf'))
        self.k = k

    def generate(self, graph):
        """
        Create a small-world graph using the given input graph.

        :param graph: The graph to use.
        :type graph: :class:`apgl.graph.AbstractMatrixGraph`

        :returns: The modified input graph.
        """
        Parameter.checkClass(graph, AbstractMatrixGraph)
        if graph.getNumEdges() != 0:
            raise ValueError('Graph must have no edges')
        if not graph.isUndirected():
            raise ValueError('Graph must be undirected')
        numVertices = graph.getNumVertices()
        for i in range(0, numVertices):
            for j in range(0, self.k):
                graph.addEdge(i, (i + j + 1) % numVertices)

        for i in range(0, numVertices):
            v = numpy.random.rand(self.k, 1)
            for j in range(0, self.k):
                if v[j] < self.p:
                    ind = numpy.random.randint(0, numVertices)
                    if graph.getEdge(i, ind) == None and ind != i:
                        graph.addEdge(i, ind)
                        graph.removeEdge(i, (i + j + 1) % numVertices)

        return graph

    def clusteringCoefficient(self):
        """
        Returns the clustering coefficient for the generator.
        """
        if self.k == 1:
            return 0
        else:
            return float(3 * (self.k - 1)) / (2 * (2 * self.k - 1)) * (1 - self.p) ** 3

    def __str__(self):
        return 'SmallWorldGenerator_p=' + str(self.p) + ',k=' + str(self.k)