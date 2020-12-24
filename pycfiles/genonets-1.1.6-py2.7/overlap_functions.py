# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/genonets/overlap_functions.py
# Compiled at: 2017-02-02 12:52:39
"""
    overlap_functions
    ~~~~~~~~~~~~~~~~~

    Contains functions used for computation of overlap.

    :author: Fahad Khalid
    :license: MIT, see LICENSE for more details.
"""

class OverlapAnalyzer:

    def __init__(self, repToGiantDict, repertoires, bitManip, isDoubleStranded, ordering_function):
        self.repToGiantDict = repToGiantDict
        self.repertoires = repertoires
        self.bitManip = bitManip
        self.isDoubelStranded = isDoubleStranded
        self.repertoires.sort(key=ordering_function)

    def getOverlapData(self):
        if len(self.repertoires) < 2:
            print 'Overlap computation triggered with only one repertoire!'
            print 'Overlap can only be calculated with 2 or more repertoires.'
            return (None, None)
        else:
            allOverlap = {rep:{seq:[] for seq in self.repToGiantDict[rep].vs['sequences']} for rep in self.repertoires}
            overlapMat = [ [ 0 for _ in range(len(self.repertoires)) ] for _ in range(len(self.repertoires))
                         ]
            for i in range(len(self.repertoires) - 1):
                giant_i = self.repToGiantDict[self.repertoires[i]]
                seqs_i = giant_i.vs['sequences']
                for j in range(i + 1, len(self.repertoires)):
                    giant_j = self.repToGiantDict[self.repertoires[j]]
                    seqs_j = giant_j.vs['sequences']
                    overlapList = self.getOverlapList(seqs_i, seqs_j)
                    overlapMat[i][j] = overlapMat[j][i] = len(overlapList)
                    if len(overlapList) > 0:
                        for sequence in overlapList:
                            allOverlap[self.repertoires[i]][sequence].append(self.repertoires[j])
                            allOverlap[self.repertoires[j]][sequence].append(self.repertoires[i])

            return (
             overlapMat, self.repertoires, allOverlap)

    def getOverlapList(self, seqs1, seqs2):
        if self.isDoubelStranded:
            rc_seqs2 = [ self.bitManip.getReverseComplement(self.bitManip.seqToBits(s)) for s in seqs2
                       ]
            rc_seqs2 = [ self.bitManip.bitsToSeq(rc) for rc in rc_seqs2 ]
            seqs2.extend(list(set(seqs2) | set(rc_seqs2)))
        return list(set(seqs1) & set(seqs2))