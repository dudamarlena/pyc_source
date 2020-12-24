# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/apgl/io/PajekWriter.py
# Compiled at: 2010-08-11 15:11:52
"""
Created on 6 Jul 2009

@author: charanpal

A class to output Pajek files from a Graph 
"""
from apgl.io.GraphWriter import GraphWriter
from apgl.util.Util import Util
import logging

class PajekWriter(GraphWriter):

    def __init__(self):
        self.colours = [
         'Cyan', 'Yellow', 'LimeGreen', 'Red', 'Blue']
        self.colours.extend(['Pink', 'White', 'Orange', 'Purple', 'CadetBlue'])
        self.colours.extend(['TealBlue', 'OliveGreen', 'Gray', 'Black', 'Maroon'])
        self.colours.extend(['LightGreen', 'LightYellow', 'Magenta', 'MidnightBlue', 'Dandelion'])
        self.defaultColour = 13
        self.vertexIdDict = {}
        self.vertexColourFunction = None
        self.edgeColourFunction = None
        self.vertexSizeFunction = None
        self.edgeSizeFunction = None
        self.edgeWeightFunction = None
        self.printStep = 100
        return

    def setVertexColourFunction(self, vertexColourFunction):
        self.vertexColourFunction = vertexColourFunction

    def setEdgeColourFunction(self, edgeColourFunction):
        self.edgeColourFunction = edgeColourFunction

    def setVertexSizeFunction(self, vertexSizeFunction):
        self.vertexSizeFunction = vertexSizeFunction

    def setEdgeSizeFunction(self, edgeSizeFunction):
        self.edgeSizeFunction = edgeSizeFunction

    def setEdgeWeightFunction(self, edgeWeightFunction):
        self.edgeWeightFunction = edgeWeightFunction

    def writeToFile(self, fileName, graph):
        fileName = fileName + '.net'
        numVertices = graph.getNumVertices()
        pajekIndex = 1
        f = open(fileName, 'w')
        f.write('*Vertices ' + str(numVertices) + '\n')
        logging.info('Writing to Pajek file: ' + fileName)
        logging.info('Writing vertices')
        for i in graph.getAllVertexIds():
            Util.printIteration(i, self.printStep, graph.getNumVertices())
            self.vertexIdDict[i] = pajekIndex
            vertexSize = self.getVertexSize(i, graph)
            vertexColour = self.getVertexColour(i, graph)
            vertexString = str(pajekIndex) + ' "' + str(pajekIndex) + '" '
            vertexString = vertexString + '0.0 0.0 0.0 '
            vertexString = vertexString + 'x_fact ' + str(vertexSize) + ' '
            vertexString = vertexString + 'y_fact ' + str(vertexSize) + ' '
            vertexString = vertexString + 'ic ' + vertexColour + ' '
            vertexString = vertexString + 'bc ' + vertexColour + ' \n'
            f.write(vertexString)
            pajekIndex += 1

        logging.info('Writing edges')
        if graph.isUndirected():
            f.write('*Edges\n')
            f.write(self.__getEdgeString(graph))
        else:
            f.write('*Arcs\n')
            f.write(self.__getArcString(graph))
        f.close()
        logging.info('Finished, wrote ' + str(numVertices) + ' vertices & ' + str(graph.getNumEdges()) + ' edges.')

    def getVertexPosition(self, vertexIndex, graph):
        return (0.0, 0.0, 0.0)

    def getVertexSize(self, vertexIndex, graph):
        if self.vertexSizeFunction == None:
            return 1
        else:
            return self.vertexSizeFunction(vertexIndex, graph)
            return

    def getVertexColour(self, vertexIndex, graph):
        if self.vertexColourFunction == None:
            return self.colours[self.defaultColour]
        else:
            return self.vertexColourFunction(vertexIndex, graph)
            return

    def getEdgeSize(self, vertexIndex1, vertexIndex2, graph):
        if self.edgeSizeFunction == None:
            return 1
        else:
            return self.edgeSizeFunction(vertexIndex1, vertexIndex2, graph)
            return

    def getEdgeColour(self, vertexIndex1, vertexIndex2, graph):
        if self.edgeColourFunction == None:
            return self.colours[self.defaultColour]
        else:
            return self.edgeColourFunction(vertexIndex1, vertexIndex2, graph)
            return

    def getEdgeWeight(self, vertexIndex1, vertexIndex2, graph):
        if self.edgeWeightFunction == None:
            return graph.getEdge(vertexIndex1, vertexIndex2)
        else:
            return self.edgeWeightFunction(vertexIndex1, vertexIndex2, graph)
            return

    def __getEdgeString(self, graph):
        edgeString = ''
        ind = 0
        for vertex1 in graph.getAllVertexIds():
            Util.printIteration(ind, self.printStep, graph.getNumVertices())
            neighbours = graph.neighbours(vertex1)
            pajekIndex1 = self.vertexIdDict[vertex1]
            for vertex2 in neighbours:
                pajekIndex2 = self.vertexIdDict[vertex2]
                colour = self.getEdgeColour(vertex1, vertex2, graph)
                edgeString = edgeString + str(pajekIndex1) + ' ' + str(pajekIndex2) + ' ' + str(self.getEdgeWeight(vertex1, vertex2, graph))
                edgeString = edgeString + ' w ' + str(self.getEdgeSize(vertex1, vertex2, graph))
                edgeString = edgeString + ' c ' + colour + '\n'

            ind = ind + 1

        return edgeString

    def __getArcString(self, graph):
        arcString = ''
        ind = 0
        for vertex1 in graph.getAllVertexIds():
            Util.printIteration(ind, self.printStep, graph.getNumVertices())
            neighbours = graph.neighbours(vertex1)
            pajekIndex1 = self.vertexIdDict[vertex1]
            for vertex2 in neighbours:
                pajekIndex2 = self.vertexIdDict[vertex2]
                arcString = arcString + str(pajekIndex1) + ' ' + str(pajekIndex2) + ' ' + str(graph.getEdge(vertex1, vertex2))
                arcString = arcString + ' c ' + self.colours[self.defaultColour] + '\n'

            ind = ind + 1

        return arcString

    defaultColour = None
    vertexIdDict = None
    colours = None