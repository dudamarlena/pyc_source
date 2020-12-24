# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/apgl/io/CsvVertexWriter.py
# Compiled at: 2010-03-03 12:27:34
"""
A class to write the vertices of a graph out to a file
"""
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