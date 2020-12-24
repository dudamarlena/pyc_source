# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/genonets/genonets_writer.py
# Compiled at: 2017-02-02 00:25:46
"""
    genonets_writer
    ~~~~~~~~~~~~~~~

    Helper functions for writing results to files.

    :author: Fahad Khalid
    :license: MIT, see LICENSE for more details.
"""
import os, copy, warnings
from genonets_constants import ErrorCodes
from genonets_exceptions import GenonetsError
from genonets_constants import GenonetsConstants as gc

class Writer:

    @staticmethod
    def writeInParamsToFile(paramsDict, path):
        fileName = path + 'in_params.txt'
        if not os.path.exists(os.path.dirname(path)):
            try:
                os.makedirs(os.path.dirname(path))
            except os.error:
                print 'Error: ' + ErrorCodes.getErrDescription(ErrorCodes.CANNOT_CREATE_DIRECTORY) + ': Path - ' + path
                raise GenonetsError(ErrorCodes.CANNOT_CREATE_DIRECTORY, 'Path - ' + path)

        try:
            with open(fileName, 'w') as (outFile):
                for param in paramsDict.keys():
                    outFile.write(param + ': ' + paramsDict[param] + '\n')

        except Exception:
            print 'Error: ' + ErrorCodes.getErrDescription(ErrorCodes.CANNOT_WRITE_TO_FILE) + ': Path - ' + path
            raise GenonetsError(ErrorCodes.CANNOT_WRITE_TO_FILE)

    @staticmethod
    def writeNetsToFile(repToNetDict, repToGiantDict, netBuilder, path, attrsToIgnore, repertoires=gc.ALL):
        if repertoires == gc.ALL:
            repertoires = repToNetDict.keys()
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        for repertoire in repertoires:
            Writer.writeNetToFile(repToNetDict[repertoire], path, attrsToIgnore)
            numComponents = len(netBuilder.getComponents(repToNetDict[repertoire]))
            if numComponents > 1:
                Writer.writeNetToFile(repToGiantDict[repertoire], path, attrsToIgnore)

    @staticmethod
    def writeNetToFile(network, path, attrsToIgnore):
        fileName = path + network['name'] + '.gml'
        netToWrite = copy.deepcopy(network)
        netAttrs = netToWrite.attributes()
        for attr in attrsToIgnore(level='network'):
            if attr in netAttrs:
                del netToWrite[attr]

        vtxAttrs = netToWrite.vs.attributes()
        for attr in attrsToIgnore(level='vertex'):
            if attr in vtxAttrs:
                del netToWrite.vs[attr]

        if not network.is_directed():
            netToWrite.vs['genotype'] = netToWrite.vs['sequences']
            netToWrite.vs['score'] = netToWrite.vs['escores']
            del netToWrite.vs['sequences']
            del netToWrite.vs['escores']
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            netToWrite.write(fileName, format='gml')

    @staticmethod
    def writeNetAttribs(repToNetDict, repToGiantDict, netBuilder, path, attrsToIgnore, attribute_order, genotype_set_order, repertoires=gc.ALL):
        if repertoires == gc.ALL:
            repertoires = repToNetDict.keys()
        attributes = repToNetDict[repertoires[0]].attributes()
        attributes.remove('name')
        numComponents = len(netBuilder.getComponents(repToNetDict[repertoires[0]]))
        if numComponents > 1:
            attributes.extend(repToGiantDict[repertoires[0]].attributes())
        for attr in attrsToIgnore():
            if attr in attributes:
                attributes.remove(attr)

        attributes.sort(key=attribute_order)
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        fileName = path + 'Genotype_set_measures.txt'
        dataFile = open(fileName, 'w')
        dataFile.write('Genotype_set\t')
        for attribute in attributes:
            dataFile.write(attribute + '\t')

        dataFile.write('\n')
        repertoires.sort(key=genotype_set_order)
        for repertoire in repertoires:
            dataFile.write(repToNetDict[repertoire]['name'] + '\t')
            for attribute in attributes:
                if attribute in repToNetDict[repertoire].attributes():
                    dataFile.write(str(repToNetDict[repertoire][attribute]) + '\t')
                else:
                    dataFile.write(str(repToGiantDict[repertoire][attribute]) + '\t')

            dataFile.write('\n')

        dataFile.close()

    @staticmethod
    def writeSeqAttribs(repToGiantDict, path, attrsToIgnore, order, repertoires=gc.ALL):
        if repertoires == gc.ALL:
            repertoires = repToGiantDict.keys()
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        for repertoire in repertoires:
            fileName = path + repertoire + '_genotype_measures.txt'
            with open(fileName, 'w') as (dataFile):
                Writer.writeSeqAttribsFor(repToGiantDict[repertoire], dataFile, attrsToIgnore, order)

    @staticmethod
    def writeSeqAttribsFor(network, dataFile, attrsToIgnore, order):
        attributes = network.vs.attributes()
        for attr in attrsToIgnore():
            if attr in attributes:
                attributes.remove(attr)

        attributes.sort(key=order)
        dataFile.write('Sequence\t')
        for attribute in attributes:
            dataFile.write(attribute + '\t')

        dataFile.write('\n')
        sequences = network.vs['sequences']
        for i in range(len(sequences)):
            dataFile.write(sequences[i] + '\t')
            for attribute in attributes:
                dataFile.write(str(network.vs[i][attribute]) + '\t')

            dataFile.write('\n')

    @staticmethod
    def writeOverlapToFile(overlapMat, repertoires, path):
        fileName = path + 'Genotype_set_overlap.txt'
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        dataFile = open(fileName, 'w')
        for repertoire in repertoires:
            dataFile.write('\t' + repertoire)

        for i in range(len(overlapMat)):
            dataFile.write('\n')
            dataFile.write(repertoires[i])
            for j in range(len(overlapMat)):
                if not i == j:
                    dataFile.write('\t' + str(overlapMat[i][j]))
                else:
                    dataFile.write('\tNaN')

        dataFile.close()