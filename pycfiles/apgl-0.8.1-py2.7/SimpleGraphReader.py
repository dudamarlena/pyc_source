# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/apgl/io/SimpleGraphReader.py
# Compiled at: 2010-07-24 12:39:22
from apgl.io.GraphReader import GraphReader
from apgl.graph.VertexList import VertexList
from apgl.graph.SparseGraph import SparseGraph
import logging

class SimpleGraphReader(GraphReader):
    """
        A class to read SimpleGraph files.
        """

    def __init__(self):
        pass

    def readFromFile(self, fileName):
        """
            Read vertices and edges of the graph from the given file name. The file
            must have as its first line "Vertices" followed by a list of
            vertex indices (one per line). Then the lines following "Arcs" or "Edges"
            have a list of pairs of vertex indices represented directed or undirected
            edges.
            """
        infile = open(fileName, 'r')
        line = infile.readline()
        line = infile.readline()
        ind = 0
        vertexIdDict = {}
        while infile and line != 'Edges' and line != 'Arcs':
            vertexIdDict[int(line)] = ind
            line = infile.readline().strip()
            ind += 1

        if line == 'Edges':
            undirected = True
        else:
            if line == 'Arcs':
                undirected = False
            else:
                raise ValueError('Unknown edge types: ' + line)
            numVertices = len(vertexIdDict)
            numFeatures = 0
            vList = VertexList(numVertices, numFeatures)
            sGraph = SparseGraph(vList, undirected)
            line = infile.readline()
            while line:
                s = line.split()
                try:
                    i = vertexIdDict[int(s[0].strip(',').strip())]
                    j = vertexIdDict[int(s[1].strip(',').strip())]
                    k = float(s[2].strip(',').strip())
                except KeyError:
                    print 'Vertex not found in list of vertices.'
                    raise

                sGraph.addEdge(i, j, k)
                line = infile.readline()

        logging.info('Read graph with ' + str(numVertices) + ' vertices and ' + str(sGraph.getNumEdges()) + ' edges')
        return sGraph