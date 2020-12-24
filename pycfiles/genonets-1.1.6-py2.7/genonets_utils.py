# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/genonets/genonets_utils.py
# Compiled at: 2017-01-31 16:34:36
"""
    genonets_utils
    ~~~~~~~~~~~~~~

    General utility functions.

    :author: Fahad Khalid
    :license: MIT, see LICENSE for more details.
"""
import numpy as np

class Utils:

    @staticmethod
    def reverseDict(inDict):
        return {inDict[key]:key for key in inDict.keys()}

    @staticmethod
    def getSeqWithMaxScore(network, seqLength):
        sortedArr = Utils.getSortedSeqEscArr(network, seqLength, sortOrder='ascending')
        return sortedArr[(-1)]['sequence']

    @staticmethod
    def getSortedSeqEscArr(network, seqLength, sortOrder):
        seqEscrArr = Utils.getSeqEscrArr(network, seqLength)
        sortedArr = np.sort(seqEscrArr, order='escore')
        if sortOrder == 'ascending':
            return sortedArr
        if sortOrder == 'descending':
            revArr = sortedArr[::-1]
            return revArr

    @staticmethod
    def getSeqEscrArr(network, seqLength):
        seqs = network.vs['sequences']
        escores = network.vs['escores']
        dtype = [
         (
          'sequence', 'S' + str(seqLength)),
         (
          'escore', float)]
        values = [ (seqs[i], escores[i]) for i in range(len(seqs)) ]
        return np.array(values, dtype=dtype)