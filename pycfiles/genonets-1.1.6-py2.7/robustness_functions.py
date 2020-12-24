# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/genonets/robustness_functions.py
# Compiled at: 2017-01-24 11:14:48
"""
    robustness_functions
    ~~~~~~~~~~~~~~~~~~~~

    Contains functions used for genotype and phenotype robustness computations.

    :author: Fahad Khalid
    :license: MIT, see LICENSE for more details.
"""
import numpy as np

class RobustnessAnalyzer:

    def __init__(self, network, netBuilder, is_double_stranded):
        self.network = network
        self.netBuilder = netBuilder
        self.bitManip = netBuilder.bitManip
        self.is_double_stranded = is_double_stranded
        self.robustnessVals = None
        return

    def getAvgRobustness(self):
        return np.mean(self.getRobustnessAll())

    def getRobustnessAll(self, recompute=False):
        if not self.robustnessVals or recompute:
            self.robustnessVals = [ self.getGenotypeRobustness(seq) for seq in self.network.vs['sequences']
                                  ]
        return self.robustnessVals

    def getGenotypeRobustness(self, sequence):
        vertex = self.netBuilder.getVertex(sequence, self.network)
        degree = self.network.degree(vertex)
        allNeighbors = self.bitManip.generateNeighbors(self.bitManip.seqToBits(sequence))
        if self.is_double_stranded:
            rc = self.bitManip.getReverseComplement(self.bitManip.seqToBits(sequence))
            if rc in allNeighbors:
                allNeighbors.remove(rc)
            for neighbor in list(allNeighbors):
                rc_n = self.bitManip.getReverseComplement(neighbor)
                if rc_n != neighbor and rc_n in allNeighbors:
                    allNeighbors.remove(neighbor)

        numNeighbors = len(allNeighbors)
        try:
            return float(degree) / float(numNeighbors)
        except ZeroDivisionError:
            return 0