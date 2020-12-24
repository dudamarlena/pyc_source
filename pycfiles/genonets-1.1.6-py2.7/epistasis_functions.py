# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/genonets/epistasis_functions.py
# Compiled at: 2017-01-31 16:34:36
"""
    evolvability_functions
    ~~~~~~~~~~~~~~~~~~~~~~

    Contains functions used for epistasis computation.

    :author: Fahad Khalid
    :license: MIT, see LICENSE for more details.
"""
from genonets_constants import EpistasisConstants as epi

class EpistasisAnalyzer:

    def __init__(self, network, netUtils, seqToEscrDict, delta, bitManip):
        self.network = network
        self.netUtils = netUtils
        self.seqToEscrDict = seqToEscrDict
        self.delta = delta
        self.bitManip = bitManip
        self.seqToVidDict = self.buildSeqToVidDict()
        self.squares = None
        self.sqrEpi = None
        return

    def getEpiAll(self):
        epistasis = {epi.MAGNITUDE: 0, epi.SIGN: 0, epi.RECIPROCAL_SIGN: 0, 
           epi.NO_EPISTASIS: 0}
        squares = self.getSquares()
        self.sqrEpi = []
        for square in squares:
            epiClass = self.getEpistasis(square)
            self.sqrEpi.append(epiClass)
            epistasis[epiClass] += 1

        del epistasis[epi.NO_EPISTASIS]
        for epiClass in epistasis.keys():
            try:
                epistasis[epiClass] = float(epistasis[epiClass]) / float(len(squares))
            except ZeroDivisionError:
                epistasis[epiClass] = 0

        return epistasis

    def getEpistasis(self, square):
        epsilon = 0
        epiClass = epi.NO_EPISTASIS
        esrc_AB = self.seqToEscrDict[square[3]]
        esrc_ab = self.seqToEscrDict[square[0]]
        esrc_Ab = self.seqToEscrDict[square[2]]
        esrc_aB = self.seqToEscrDict[square[1]]
        epsilon = esrc_AB + esrc_ab - esrc_Ab - esrc_aB
        if abs(epsilon) >= self.delta:
            epiClass = self.getEpiClass(esrc_ab, esrc_aB, esrc_Ab, esrc_AB)
            if epiClass == epi.NO_EPISTASIS:
                epsilon = 0
        else:
            epsilon = 0
        return epiClass

    def getEpiClass(self, esrc_ab, esrc_aB, esrc_Ab, esrc_AB):
        epiClass = 0
        dE_ab_Ab = esrc_Ab - esrc_ab
        dE_aB_AB = esrc_AB - esrc_aB
        dE_ab_aB = esrc_aB - esrc_ab
        dE_Ab_AB = esrc_AB - esrc_Ab
        dE_ab_Ab = dE_ab_Ab if abs(dE_ab_Ab) >= self.delta else 0
        dE_aB_AB = dE_aB_AB if abs(dE_aB_AB) >= self.delta else 0
        dE_ab_aB = dE_ab_aB if abs(dE_ab_aB) >= self.delta else 0
        dE_Ab_AB = dE_Ab_AB if abs(dE_Ab_AB) >= self.delta else 0
        if dE_ab_Ab == 0 and dE_aB_AB == 0 and dE_ab_aB == 0 and dE_Ab_AB == 0:
            return epi.NO_EPISTASIS
        condition1 = abs(dE_ab_Ab + dE_aB_AB) == abs(dE_ab_Ab) + abs(dE_aB_AB)
        condition2 = abs(dE_ab_aB + dE_Ab_AB) < abs(dE_ab_aB) + abs(dE_Ab_AB)
        if condition1 and not condition2:
            epiClass = epi.MAGNITUDE
        elif condition2 and not condition1:
            epiClass = epi.RECIPROCAL_SIGN
        else:
            epiClass = epi.SIGN
        return epiClass

    def buildSeqToVidDict(self):
        sequences = self.network.vs['sequences']
        return {sequences[i]:i for i in range(len(sequences))}

    def getSquares(self, recompute=False):
        if self.squares and not recompute:
            return self.squares
        squares = []
        bitSqrs = set()
        sequences = self.network.vs['sequences']
        for sequence in sequences:
            neighbors = [ self.network.vs[vid]['sequences'] for vid in self.network.neighbors(self.netUtils.getVertex(sequence, self.network))
                        ]
            if len(neighbors) < 2:
                continue
            pairs = [ (neighbors[i], neighbors[j]) for i in range(len(neighbors) - 1) for j in range(i + 1, len(neighbors)) if not self.netUtils.areConnected(neighbors[i], neighbors[j])
                    ]
            for pair in pairs:
                commonNeighs = self.getCommonNeighbors(pair, sequence)
                for node in commonNeighs:
                    if node not in neighbors:
                        square = [sequence, pair[0], pair[1], node]
                        bitSqr = frozenset([self.bitManip.seqToBits(sequence),
                         self.bitManip.seqToBits(pair[0]),
                         self.bitManip.seqToBits(pair[1]),
                         self.bitManip.seqToBits(node)])
                        if bitSqr not in bitSqrs:
                            squares.append(square)
                            bitSqrs.add(bitSqr)

        self.squares = squares
        return squares

    def getCommonNeighbors(self, pair, parent):
        neighbors1 = [ self.network.vs[vid]['sequences'] for vid in self.network.neighbors(self.seqToVidDict[pair[0]])
                     ]
        neighbors2 = [ self.network.vs[vid]['sequences'] for vid in self.network.neighbors(self.seqToVidDict[pair[1]])
                     ]
        commonNeighbors = list(set(neighbors1) & set(neighbors2))
        commonNeighbors.remove(parent)
        return commonNeighbors

    def getVertexToSquaresDict(self):
        if not self.squares or len(self.squares) < 1:
            return ({}, [])
        sequences = self.network.vs['sequences']
        vtxToSqrs = {vId:[] for vId in range(len(sequences))}
        squares = []
        for sqrIndx in range(len(self.squares)):
            sqr = []
            for sequence in self.squares[sqrIndx]:
                seqIndx = sequences.index(sequence)
                vtxToSqrs[seqIndx].append(sqrIndx)
                sqr.append(seqIndx)

            squares.append(sqr)

        return (vtxToSqrs, squares)

    def getSqrEpi(self):
        return self.sqrEpi