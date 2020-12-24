# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ProDaMa/SimilaritySearchEngine.py
# Compiled at: 2009-10-06 08:43:40
"""
To perform search by homology sequence
"""
from ProDaMa.services.PDBClient import *
from ProDaMa.services.PSIBlast import callPSIBlast

class SimilaritySearchEngine(object):
    """
    Performs search by homology sequence.
    """

    def PSIBlast(self, sequence, ecutoff, iterations):
        """
        Performs a PSI-BLAST homology search
        
        arguments:
            sequence: the target sequence
            
            ecutoff: the E-value 
            
            iterations: the number of PSI-BLAST iterations
        
        return:
            a list of protein identifiers in the form of tuples (structure, chain).
        """
        return callPSIBlast(sequence, ecutoff, iterations)

    def FASTA(self, sequence, ecutoff):
        """
        Performs a FASTA homology search.
        
        arguments:
            sequence: the target sequence 
            
            ecutoff: the E-value 
        
        return:
            a list of protein identifiers in the form of tuples  (structure, chain).
        """
        return [ (chain_id.split(':')[0], '_ABCDEFGHIJKLMNOPQRSTUVWXYZ'[int(chain_id.split(':')[1])]) for chain_id in PDBClient().fastaQuery(sequence, ecutoff) ]