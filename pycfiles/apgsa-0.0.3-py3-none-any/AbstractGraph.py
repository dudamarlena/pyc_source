# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/apgl/graph/AbstractGraph.py
# Compiled at: 2012-07-13 12:04:09
__doc__ = '\nCreated on 15 Feb 2010\n\n@author: charanpal\n'
from apgl.util.Util import Util

class AbstractGraph(object):
    """
    A very basic abstract base class for graphs.
    """

    def density(self):
        """
        The density of the graph is the number of edges/number of possible edges,
        which does not include self loops. The density of a graph with no vertices
        is zero.

        :returns: The density of the graph. 
        """
        n = self.getNumVertices()
        m = self.getNumEdges()
        if n == 1 or n == 0:
            return m
        if self.isUndirected():
            return float(2 * m) / (n * (n - 1))
        else:
            return float(m) / (n * (n - 1))

    def getNumEdges(self):
        """ Returns the total number of edges in the graph. """
        Util.abstract()

    def getNumVertices(self):
        """ Returns the total number of vertices in the graph. """
        Util.abstract()

    def isUndirected(self):
        """
        :returns: true if the current graph is undirected, otherwise false.
        """
        Util.abstract()

    def neighbours(self, vertexIndex):
        """ Return a iterable item of neighbours (indices) """
        Util.abstract()

    def getVertex(self, vertexIndex):
        """ Return a vertex of given index """
        Util.abstract()

    def getAllVertexIds(self):
        """
        :returns: all indices of the vertices of the graph.
        """
        Util.abstract()

    def setVertex(self, vertexIndex, vertex):
        """ Assign a value to a vertex """
        Util.abstract()

    def getAllEdges(self):
        """
        Return an array of edges with each row representing an edge and its type index.
        """
        Util.abstract()

    def subgraph(self, vertexIndices):
        """
        Takes a list of vertex indices and returns the subgraph containing those
        indices. 
        """
        Util.abstract()

    size = property(getNumVertices, doc='The number of vertices in the graph')