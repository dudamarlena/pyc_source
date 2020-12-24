# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/apgl/io/CsvVertexWriter.py
# Compiled at: 2010-03-03 12:27:34
__doc__ = '\nA class to write the vertices of a graph out to a file\n'
import csv, logging

class CsvVertexWriter:

    def __init__(self):
        pass

    def writeToFile(self, fileName, graph):
        logging.info('Writing to file: ' + fileName + '.csv')
        indices = graph.getAllVertexIds()
        writer = csv.writer(open(fileName + '.csv', 'w'), delimiter=',', lineterminator='\n')
        for i in indices:
            writer.writerow(graph.getVertex(i))

        logging.info('Wrote ' + str(graph.getNumVertices()) + ' vertices.')