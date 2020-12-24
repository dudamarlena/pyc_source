# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ProDaMa/IdentitySearchEngine.py
# Compiled at: 2009-10-06 08:40:45
"""
To perform search by identity sequence.
"""
from ProDaMa.services.PISCESInterface import cullFromPDB
from ProDaMa.model.dbSession import *

class IdentitySearchEngine(object):
    """
    Performs search by identity sequence.
    """

    def __init__(self, protein_ids=None):
        """
        Initializes the set of proteins to be analyzed.
            
        arguments:            
            protein_ids: a list of protein identifiers in the form of tuples (structure, chain). By default (protein_ids=None) all proteins are examined. 
            
        """
        self.__ids = protein_ids

    def setProteinIds(self, protein_ids=None):
        """
        Initializes the set of proteins to be analyzed.

        arguments:
            protein_ids: a list of protein identifiers in the form of tuples (structure, chain). By default (protein_ids=None) all proteins are examined.

        """
        self.__ids = protein_ids

    def sequencesCullFromPDB(self, **parameters):
        """
        Culls (using PISCES) sets of protein sequences from the overall local database or from a specified subset according to sequence identity and structural criteria. 
            
        arguments:
            **parameters: the PISCES parameters. By default the following parameters are used:
                    'MAX_percentage_identity'=25,
                    'MIN_resolution'=0.0,
                    'MAX_resolution'=2.5,
                    'MIN_chain_length'=20,
                    'MAX_chain_length'=10000,
                    'RFactor'=0.3,
                    'skip_non_x'=True, 
                    'skip_CA_only'=True
                    
        return:
            a list of protein identifiers in the form of tuples (structure, chain).
        """
        protein_ids = self.__ids and [ '%s%s' % protein_id for protein_id in self.__ids ] or [ '%s%s' % (chain.str_id, chain.chain_id) for chain in Session.query(Chain).all() ]
        interface_parameters = (',').join([ "%s=parameters['%s']" % (parameter, parameter) for parameter in parameters ])
        exec 'culled=cullFromPDB(protein_ids,%s)' % interface_parameters
        return [ (protein_id[:4], protein_id[(-1)]) for protein_id in culled ]