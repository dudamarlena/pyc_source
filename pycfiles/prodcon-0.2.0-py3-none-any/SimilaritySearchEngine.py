# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/ProDaMa/SimilaritySearchEngine.py
# Compiled at: 2009-10-06 08:43:40
__doc__ = '\nTo perform search by homology sequence\n'
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