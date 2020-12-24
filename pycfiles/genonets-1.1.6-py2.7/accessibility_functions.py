# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/genonets/accessibility_functions.py
# Compiled at: 2017-01-31 16:34:36
"""
    accessibility_functions
    ~~~~~~~~~~~~~~~~~~~~~~~

    Exposes functions for accessibility, neighbor abundance, and diversity index computation.

    :author: Fahad Khalid
    :license: MIT, see LICENSE for more details.
"""

class AccessibilityAnalyzer:

    def __init__(self, repertoire, network, repToGiantDict, dataDict, netBuilder, bitManip, isDoubleStranded):
        self.repertoire = repertoire
        self.network = network
        self.repToGiantDict = repToGiantDict
        self.dataDict = dataDict
        self.netBuilder = netBuilder
        self.bitManip = bitManip
        self.isDoubelStranded = isDoubleStranded

    def getAccessibility(self):
        accessibility = 0
        targets = self.dataDict.keys()
        targets.remove(self.repertoire)
        sequences = [ self.bitManip.seqToBits(seq) for seq in self.network.vs['sequences']
                    ]
        if self.isDoubelStranded:
            sequences.extend([ self.bitManip.getReverseComplement(seq) for seq in sequences
                             ])
        for target in targets:
            targetNet = self.repToGiantDict[target]
            extNeighbors = self.netBuilder.getAllExtNeighbors(targetNet)
            commonSeqs = set(extNeighbors) & set(sequences)
            try:
                fraction = float(len(commonSeqs)) / float(len(extNeighbors))
            except ZeroDivisionError:
                fraction = 0

            accessibility += fraction

        return accessibility

    def getNeighborAbundance(self):
        abundance = 0
        extNeighbors = self.netBuilder.getAllExtNeighbors(self.network)
        targets = self.dataDict.keys()
        targets.remove(self.repertoire)
        for target in targets:
            targetSeqs = [ self.bitManip.seqToBits(seq) for seq in self.repToGiantDict[target].vs['sequences']
                         ]
            if self.isDoubelStranded:
                targetSeqs.extend([ self.bitManip.getReverseComplement(seq) for seq in targetSeqs
                                  ])
            commonSeqs = set(extNeighbors) & set(targetSeqs)
            try:
                fraction = float(len(commonSeqs)) / float(len(extNeighbors))
            except ZeroDivisionError:
                fraction = 0

            abundanceFrac = float(fraction) * float(len(set(targetSeqs)))
            abundance += abundanceFrac

        return abundance

    def getPhenotypicDivesity(self):
        diversity = 0
        extNeighbors = self.netBuilder.getAllExtNeighbors(self.network)
        targets = self.dataDict.keys()
        targets.remove(self.repertoire)
        for target in targets:
            targetSeqs = [ self.bitManip.seqToBits(seq) for seq in self.repToGiantDict[target].vs['sequences']
                         ]
            if self.isDoubelStranded:
                targetSeqs.extend([ self.bitManip.getReverseComplement(seq) for seq in targetSeqs
                                  ])
            commonSeqs = set(extNeighbors) & set(targetSeqs)
            try:
                fraction = float(len(commonSeqs)) / float(len(extNeighbors))
            except ZeroDivisionError:
                fraction = 0

            diversity += fraction * fraction

        return diversity