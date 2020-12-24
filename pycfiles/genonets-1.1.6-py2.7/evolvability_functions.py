# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/genonets/evolvability_functions.py
# Compiled at: 2017-01-31 16:34:36
"""
    evolvability_functions
    ~~~~~~~~~~~~~~~~~~~~~~

    Contains functions used for genotype and phenotype evolvability computations.

    :author: Fahad Khalid
    :license: MIT, see LICENSE for more details.
"""

class EvolvabilityAnalyzer:

    def __init__(self, network, dataDict, seqToRepDict, repToGiantDict, rcToSeqDict, bitsToSeqDict, netBuilder, isDoubleStranded):
        self.network = network
        self.dataDict = dataDict
        self.seqToRepDict = seqToRepDict
        self.repToGiantDict = repToGiantDict
        self.rcToSeqDict = rcToSeqDict
        self.bitsToSeqDict = bitsToSeqDict
        self.netBuilder = netBuilder
        self.isDoubleStranded = isDoubleStranded
        self.bm = self.netBuilder.bitManip
        self.evoTuples = None
        return

    @staticmethod
    def updateSeqToRepDict(seqToRepDict_original, repToGiantDict):
        seqToRepDict = seqToRepDict_original.copy()
        for seq in seqToRepDict.keys():
            seqToRepDict[seq] = [ rep for rep in seqToRepDict[seq] if seq in repToGiantDict[rep].vs['sequences']
                                ]

        return seqToRepDict

    @staticmethod
    def buildRcToSeqDict(seqToRepDict, bm):
        rcToSeqDict = dict()
        for seq in seqToRepDict.keys():
            rcBitSeq = bm.getReverseComplement(bm.seqToBits(seq))
            rcToSeqDict[rcBitSeq] = seq

        return rcToSeqDict

    @staticmethod
    def buildBitsToSeqDict(seqToRepDict, rcToSeqDict, bm, isDoubleStranded):
        bitsToSeqDict = {bm.seqToBits(seq):seq for seq in seqToRepDict.keys()}
        if isDoubleStranded:
            for rc in rcToSeqDict.keys():
                bitsToSeqDict[rc] = bm.bitsToSeq(rc)

        return bitsToSeqDict

    def getReportoireEvo(self):
        evoTuples = self.getEvoAll()
        repLists = [ evoTuples[1].keys() for evoTuples in evoTuples if evoTuples[1]
                   ]
        targets = []
        for repList in repLists:
            targets.extend([ target for target in repList ])

        targets = list(set(targets))
        try:
            evolvability = float(len(targets)) / float(len(self.dataDict) - 1)
            return (
             evolvability, targets)
        except ZeroDivisionError:
            return (
             0, targets)

    def getEvoAll(self, recompute=False):
        if not self.evoTuples or recompute:
            self.evoTuples = [ self.getSeqEvo(seq) for seq in self.network.vs['sequences']
                             ]
        return self.evoTuples

    def getSeqEvo(self, sequence):
        externNeighbors = self.netBuilder.getExternalNeighbors(sequence, self.network)
        targetReps = self.getEvoTargetReps(externNeighbors)
        try:
            evolvability = float(len(targetReps)) / float(len(self.dataDict) - 1)
        except ZeroDivisionError:
            evolvability = 0

        return (evolvability, targetReps)

    def getEvoTargetReps(self, extNeighs):
        targetReps = dict()
        for extNeigh in extNeighs:
            try:
                extNeighSeq = self.bitsToSeqDict[extNeigh]
            except KeyError:
                continue

            if extNeighSeq in self.seqToRepDict:
                self.appendToTargets(extNeighSeq, targetReps)
            elif self.isDoubleStranded:
                extNeighBits = self.bm.seqToBits(extNeighSeq)
                if extNeighBits in self.rcToSeqDict:
                    strSeq = self.rcToSeqDict[extNeighBits]
                    self.appendToTargets(strSeq, targetReps)

        return targetReps

    def appendToTargets(self, seq, targetReps):
        for repertoire in self.seqToRepDict[seq]:
            if self.network['name'] in [repertoire, repertoire + '_dominant']:
                continue
            if repertoire not in targetReps:
                targetReps[repertoire] = []
            targetReps[repertoire].append(seq)