# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/genonets/seq_bit_impl.py
# Compiled at: 2016-07-23 05:10:02
"""
    seq_bit_impl
    ~~~~~~~~~~~~

    Contains classes that define alphabet types that can be used with
    the bit manipulation library.

    :author: Fahad Khalid
    :license: MIT, see LICENSE for more details.
"""
from seq_bit_lib import AbstractBitSeqManipulator
from genonets_utils import Utils

class BinaryBitSeqManipulator(AbstractBitSeqManipulator):
    bitCodeLen = 1
    letterToBitDict = {'0': 0, '1': 1}
    bitToLetterDict = Utils.reverseDict(letterToBitDict)


class ProteinBitSeqManipulator(AbstractBitSeqManipulator):
    bitCodeLen = 5
    letterToBitDict = {'A': 0, 
       'R': 1, 'N': 2, 'D': 3, 'C': 4, 'E': 5, 
       'Q': 6, 'G': 7, 'H': 8, 'I': 9, 'L': 10, 
       'K': 11, 'M': 12, 'F': 13, 'P': 14, 'S': 15, 
       'T': 16, 'W': 17, 'Y': 18, 'V': 19}
    bitToLetterDict = Utils.reverseDict(letterToBitDict)


class AbstractXnaBitSeqManipulator(AbstractBitSeqManipulator):
    bitCodeLen = 2


class RNABitSeqManipulator(AbstractXnaBitSeqManipulator):
    letterToBitDict = {'A': 0, 'U': 1, 'C': 2, 'G': 3}
    bitToLetterDict = {0: 'A', 1: 'U', 2: 'C', 3: 'G'}


class DNABitSeqManipulator(AbstractXnaBitSeqManipulator):
    letterToBitDict = {'A': 0, 'T': 1, 'C': 2, 'G': 3}
    bitToLetterDict = {0: 'A', 1: 'T', 2: 'C', 3: 'G'}
    baseToComplementDict = {0: 1, 1: 0, 2: 3, 3: 2}

    def __init__(self, seqLength, useIndels, use_reverse_complements):
        AbstractXnaBitSeqManipulator.__init__(self, seqLength, useIndels)
        self.useRC = use_reverse_complements

    def getReverseComplement(self, sequence):
        revCompl = 0
        for i in reversed(range(self.seqLength)):
            bitValue = self.getLetterAtIndex(sequence, i)
            revCompl |= self.baseToComplementDict[bitValue]
            if i != 0:
                revCompl <<= 2

        return revCompl

    def areNeighbors(self, seq1, seq2):
        if AbstractXnaBitSeqManipulator.areNeighbors(self, seq1, seq2):
            return True
        if self.useRC:
            revComplSeq2 = self.getReverseComplement(seq2)
            if AbstractXnaBitSeqManipulator.areNeighbors(self, seq1, revComplSeq2):
                return True
        return False


class BitManipFactory:
    moleculeTypes = [
     'RNA', 'DNA', 'Protein', 'Binary']

    @staticmethod
    def getMoleculeTypes():
        return BitManipFactory.moleculeTypes

    @staticmethod
    def getBitSeqManip(moleculeType, seqLength, useIndels, useReverseComplements=False):
        if moleculeType == 'RNA':
            return RNABitSeqManipulator(seqLength, useIndels)
        if moleculeType == 'DNA':
            return DNABitSeqManipulator(seqLength, useIndels, useReverseComplements)
        if moleculeType == 'Protein':
            return ProteinBitSeqManipulator(seqLength, useIndels)
        if moleculeType == 'Binary':
            return BinaryBitSeqManipulator(seqLength, useIndels)
        print 'Unsupported moleculeType: ' + str(moleculeType)
        print 'Exiting program ...'
        exit()