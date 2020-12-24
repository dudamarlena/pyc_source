# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/apgl/graph/Benchmark.py
# Compiled at: 2012-12-20 11:10:14
__doc__ = '\nA set of benchmark tests in order to compare the speed of algorithms under different \ngraph types. \n'
import numpy, logging, time, networkx
from apgl.graph import DenseGraph, SparseGraph, PySparseGraph, DictGraph
from exp.sandbox.graph.CsArrayGraph import CsArrayGraph
numpy.set_printoptions(suppress=True, precision=4)

class GraphIterator:

    def __init__(self, numVertices, sparseOnly=False, numEdges=0):
        self.numVertices = numVertices
        self.sparseOnly = sparseOnly
        self.graphList = []
        if not self.sparseOnly:
            self.graphList.append(DenseGraph(numVertices))
        self.graphList.append(PySparseGraph(numVertices))
        self.graphList.append(DictGraph())
        self.i = 0

    def __iter__(self):
        return self

    def next(self):
        if self.i == len(self.graphList):
            raise StopIteration
        else:
            graph = self.graphList[self.i]
            self.i += 1
            return graph

    def getNumGraphs(self):
        return len(self.graphList)


def generateEdges():
    edgeList = []
    density = 0.01
    numVertices = numpy.array([100, 200, 500, 1000])
    for i in numVertices:
        numEdges = i ** 2 * density
        edges = numpy.zeros((numEdges, 2))
        edges[:, 0] = numpy.random.randint(0, i, numEdges)
        edges[:, 1] = numpy.random.randint(0, i, numEdges)
        edgeList.append((i, edges))

    return edgeList


def benchmark(edgeList):
    iterator = GraphIterator(100)
    numGraphTypes = iterator.getNumGraphs()
    numMeasures = 6
    timeArray = numpy.zeros((len(edgeList), numGraphTypes, numMeasures))
    i = 0
    nxGraph = networkx.Graph()
    for numVertices, edges in edgeList:
        print 'Timing graphs of size ' + str(numVertices) + ' with ' + str(edges.shape[0]) + ' edges'
        iterator = GraphIterator(numVertices)
        j = 0
        for graph in iterator:
            measureInd = 0
            print 'Add edges benchmark on ' + str(graph)
            startTime = time.clock()
            for m in range(10):
                graph.addEdges(edges)

            timeArray[(i, j, measureInd)] = time.clock() - startTime
            measureInd += 1
            vertexIds = graph.getAllVertexIds()
            print 'Neighbours benchmark on ' + str(graph)
            startTime = time.clock()
            for m in range(100):
                for k in range(50):
                    graph.neighbours(vertexIds[k])

            timeArray[(i, j, measureInd)] = time.clock() - startTime
            measureInd += 1
            print 'Depth first search benchmark on ' + str(graph)
            startTime = time.clock()
            for k in range(5):
                graph.depthFirstSearch(vertexIds[k])

            timeArray[(i, j, measureInd)] = time.clock() - startTime
            measureInd += 1
            print 'Breadth first search benchmark on ' + str(graph)
            startTime = time.clock()
            for k in range(5):
                graph.breadthFirstSearch(vertexIds[k])

            timeArray[(i, j, measureInd)] = time.clock() - startTime
            measureInd += 1
            print 'Find components benchmark on ' + str(graph)
            startTime = time.clock()
            graph.findConnectedComponents()
            timeArray[(i, j, measureInd)] = time.clock() - startTime
            measureInd += 1
            print 'Degree sequence benchmark on ' + str(graph)
            startTime = time.clock()
            for k in range(100):
                graph.degreeSequence()

            timeArray[(i, j, measureInd)] = time.clock() - startTime
            measureInd += 1
            j += 1

        i += 1

    return timeArray


edgeList = generateEdges()
timeArray = benchmark(edgeList)
for i in range(timeArray.shape[2]):
    print timeArray[:, :, i]