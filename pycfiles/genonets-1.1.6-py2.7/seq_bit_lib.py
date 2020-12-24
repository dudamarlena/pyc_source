# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/genonets/seq_bit_lib.py
# Compiled at: 2017-01-31 16:34:36
"""
    seq_bit_lib
    ~~~~~~~~~~~

    Library of functions for manipulation of genotypes as bits.

    :author: Fahad Khalid
    :license: MIT, see LICENSE for more details.
"""
from array import array

class AbstractBitSeqManipulator:

    def __init__(self, seqLength, useIndels):
        self.seqLength = seqLength
        self.useIndels = useIndels
        self.startIndices = self.computeStartIndices()
        self.masks = self.getMasks()

    def popcount(self, x):
        return bin(x).count('1')

    def letterToBits(self, letter):
        return self.letterToBitDict[letter]

    def bitsToLetter(self, bits):
        return self.bitToLetterDict[bits]

    def isEven(self, x):
        return x % 2 == 0

    def computeStartIndices(self):
        n = self.bitCodeLen
        l = n * self.seqLength
        indices = [ x for x in range(n - 1, l, n) ]
        return indices

    def getMasks(self):
        masks = []
        for i in range(self.bitCodeLen):
            if i == 0:
                masks.append(self.generateMask(1))
            else:
                masks.append(self.generateMask(2 << i - 1))

        return masks

    def generateMask(self, maskVal):
        l = self.bitCodeLen * self.seqLength
        mask = 0
        for i in reversed(range(0, l, self.bitCodeLen)):
            mask |= maskVal << i

        return mask

    def areNeighbors(self, seq1, seq2):
        if self.distanceBwSeqs(seq1, seq2) == 1:
            return True
        else:
            if not self.useIndels:
                return False
            rmn = self.getLetterAtIndex(seq2, self.seqLength - 1)
            temp = seq1 << self.bitCodeLen
            if seq2 == self.mutAftrLftShift(temp, self.seqLength - 1, rmn):
                return True
            lmn = self.getLetterAtIndex(seq2, 0)
            temp = seq1 >> self.bitCodeLen
            if seq2 == self.mutateLetter(temp, 0, lmn):
                return True
            return False

    def generateNeighbors(self, sequence):
        k = self.seqLength
        neighbors = [ self.mutateLetter(sequence, i, target) for i in range(k) for target in self.bitToLetterDict.keys() if target != self.getLetterAtIndex(sequence, i)
                    ]
        if self.useIndels:
            temp = sequence << self.bitCodeLen
            lsNeighbors = self.getShiftMutants('left', temp)
            neighbors.extend(self.getUniqueNeighbors(lsNeighbors, neighbors, sequence))
            temp = sequence >> self.bitCodeLen
            rsNeighbors = self.getShiftMutants('right', temp)
            neighbors.extend(self.getUniqueNeighbors(rsNeighbors, neighbors, sequence))
        return neighbors

    def getShiftMutants(self, shiftType, source):
        if shiftType == 'left':
            index = self.seqLength - 1
            mutants = [ self.mutAftrLftShift(source, index, target) for target in self.bitToLetterDict.keys()
                      ]
        else:
            index = 0
            mutants = [ self.mutateLetter(source, index, target) for target in self.bitToLetterDict.keys()
                      ]
        return mutants

    def getUniqueNeighbors(self, newNeighbors, neighbors, source):
        return [ neighbor for neighbor in newNeighbors if neighbor not in neighbors and neighbor != source
               ]

    def distanceBwSeqs(self, seq1, seq2):
        n = self.bitCodeLen
        diffList = self.buildDiffList(seq1, seq2)
        allOred = 0
        for i in range(len(diffList)):
            allOred |= diffList[i] << n - i

        distance = self.popcount(allOred)
        return distance

    def buildDiffList(self, seq1, seq2):
        diffList = []
        diffBits = seq1 ^ seq2
        for i in range(self.bitCodeLen):
            diffList.append(diffBits & self.masks[i])

        return diffList

    def mutAftrLftShift(self, sequence, position, target):
        mutant = self.mutateLetter(sequence, position, target)
        mutant = self.mutateLetter(mutant, -1, 0)
        return mutant

    def mutateLetter(self, sequence, position, target):
        n = self.bitCodeLen
        l = n * self.seqLength
        ones = (1 << n) - 1
        bitIndex = l - n - n * position
        mask = ones << bitIndex
        mutatedSeq = sequence & ~mask | target << bitIndex
        return mutatedSeq

    def getLetterAtIndex(self, sequence, index):
        l = self.bitCodeLen * self.seqLength
        i = l - 1 - index * self.bitCodeLen
        letter = self.getbitsOnIndex(i, sequence)
        return letter

    def seqToBits(self, sequence):
        bitSequence = 0
        for i in range(0, self.seqLength):
            bitValue = self.letterToBitDict[sequence[i]]
            bitSequence |= bitValue
            if i != self.seqLength - 1:
                bitSequence <<= self.bitCodeLen

        return bitSequence

    def bitsToSeq(self, bitSequence):
        k = self.seqLength
        outputSequence = array('c', [ '0' for _ in range(k) ])
        j = k - 1
        for i in self.startIndices:
            letter = self.getbitsOnIndex(i, bitSequence)
            outputSequence[j] = self.bitToLetterDict[letter]
            j -= 1

        return outputSequence.tostring()

    def getbitsOnIndex(self, i, bitSeq):
        n = self.bitCodeLen
        letter = (bitSeq & 1 << i) >> i
        for p in range(1, n):
            letter <<= 1
            letter |= (bitSeq & 1 << i - p) >> i - p

        return letter