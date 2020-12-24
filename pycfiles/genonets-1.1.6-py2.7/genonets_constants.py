# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/genonets/genonets_constants.py
# Compiled at: 2017-01-31 16:34:36
"""
    Defines constants used throughout the `Genonets` package.

    Constants are grouped into different classes according to function.

    :author: Fahad Khalid
    :license: MIT, see LICENSE for more details.
"""
from genonets_utils import Utils

class GenonetsConstants:
    ALL = 0


class SupportedAlphabet:
    """
    Names of the supported alphabet types.
    """
    binary = [
     '0', '1']
    rna = ['A', 'U', 'C', 'G']
    dna = ['A', 'T', 'C', 'G']
    protein = ['A', 'R', 'N', 'D', 'C', 'E', 'Q', 'G', 'H', 'I',
     'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V']
    typeToList = {'RNA': rna, 'DNA': dna, 'Binary': binary, 'Protein': protein}

    @staticmethod
    def getAlphabet(alphabetType):
        """
        Get the list of letters corresponding to the given alphabet type.

        :param alphabetType: One of the following strings (case sensitive),
        * RNA
        * DNA
        * Binary
        * Protein

        :return: list: List of all letters contained in the alphabet type received
                        as argument.
        """
        return SupportedAlphabet.typeToList[alphabetType]


class EpistasisConstants:
    NO_EPISTASIS = 0
    MAGNITUDE = 1
    SIGN = 2
    RECIPROCAL_SIGN = 3
    epiToDesc = {MAGNITUDE: 'Magnitude epistasis', 
       SIGN: 'Sign epistasis', 
       RECIPROCAL_SIGN: 'Reciprocal sign epistasis', 
       NO_EPISTASIS: 'No epistasis'}

    @staticmethod
    def getDesciption(epiType):
        try:
            return EpistasisConstants.epiToDesc[epiType]
        except KeyError:
            return ''


class AnalysisConstants:
    ALL = 0
    LANDSCAPE = 1
    PEAKS = 2
    PATHS = 3
    EPISTASIS = 4
    ROBUSTNESS = 5
    EVOLVABILITY = 6
    ACCESSIBILITY = 7
    NEIGHBOR_ABUNDANCE = 8
    PHENOTYPIC_DIVERSITY = 9
    STRUCTURE = 10
    OVERLAP = 11
    PATHS_RATIOS = 12
    analysisToDesc = {PEAKS: 'Peaks', 
       PATHS: 'Paths', 
       PATHS_RATIOS: 'Paths ratios', 
       EPISTASIS: 'Epistasis', 
       ROBUSTNESS: 'Robustness', 
       EVOLVABILITY: 'Evolvability', 
       ACCESSIBILITY: 'Accessibility', 
       NEIGHBOR_ABUNDANCE: 'Neighbor Abundance', 
       PHENOTYPIC_DIVERSITY: 'Diversity Index', 
       STRUCTURE: 'Structure', 
       OVERLAP: 'Overlap'}

    @staticmethod
    def getAnalysisTypes():
        return Utils.reverseDict(AnalysisConstants.analysisToDesc)


class ErrorCodes:
    UNKNOWN_ERROR = 5000
    UNKNOWN_PARSING_ERROR = 400
    INCONSISTENT_HEADER = 500
    MISSING_VALUE = 501
    BAD_SCORE_FORMAT = 502
    BAD_DELTA_FORMAT = 503
    INCONSISTENT_SEQ_LEN = 504
    ALPHABET_TYPE_MISMATCH = 505
    NO_USABLE_SCORES = 506
    RC_ALPHABET_MISMATCH = 507
    CANNOT_WRITE_TO_FILE = 550
    CANNOT_CREATE_DIRECTORY = 551
    NOT_ENOUGH_REPS_OLAP = 700
    errCodeToDesc = {UNKNOWN_ERROR: 'Something went wrong while performing analyses', 
       UNKNOWN_PARSING_ERROR: 'Something went wrong during input file parsing', 
       INCONSISTENT_HEADER: 'Input file parsing error - Column headers are not consistent with specification', 
       MISSING_VALUE: 'Input file parsing error - Missing value encountered in input file', 
       BAD_SCORE_FORMAT: 'Input file parsing error - Score value is not in the supported format', 
       BAD_DELTA_FORMAT: 'Input file parsing error - Delta value is not in the supported format', 
       INCONSISTENT_SEQ_LEN: 'Input file parsing error - Inconsistent genotype length encountered. ' + 'All genotypes must be of equal length', 
       ALPHABET_TYPE_MISMATCH: 'Input file parsing error - Genotype consists of at least one letter not ' + 'in the selected alphabet type', 
       NO_USABLE_SCORES: 'Input file parsing error - No genotypes found with score values greater than', 
       NOT_ENOUGH_REPS_OLAP: 'Analysis error - Overlap computation can only be performed if there are least ' + 'two phenotypes that have genotypes with Score values greater than Tau', 
       CANNOT_WRITE_TO_FILE: 'Could not write to file', 
       CANNOT_CREATE_DIRECTORY: 'Error while trying to create directory', 
       RC_ALPHABET_MISMATCH: 'Reverse complements can only be considered if alphabet type is DNA'}

    @staticmethod
    def getErrDescription(errCode):
        try:
            return ErrorCodes.errCodeToDesc[errCode]
        except KeyError:
            return ''