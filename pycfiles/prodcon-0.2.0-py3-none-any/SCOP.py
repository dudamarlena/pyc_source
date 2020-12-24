# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/ProDaMa/SCOP.py
# Compiled at: 2009-10-06 08:43:29
__doc__ = '\nTo search for SCOP classified proteins.\n'
from ProDaMa.model.dbSession import *

class SCOP(object):
    """
    This class provides search methods applied to the local database for selecting proteins according to a given constraint on their SCOP classification.
    """

    def __init__(self, protein_ids=None):
        """
        Initializes the set of proteins to be analyzed.
            
        arguments:            
            protein_ids: a list of protein identifiers in the form of tuples (structure, chain). By default (protein_ids=None) the set of proteins to be analyzed coincides with all proteins in the database.             
        """
        self.__ids = protein_ids

    def setProteinIds(self, protein_ids):
        """
        Permits to change the set of proteins to be analyzed.
            
        arguments:            
            protein_ids: a list of protein identifiers in the form of tuples (structure, chain).
        """
        self.__ids = protein_ids

    def __lookFor(self, level, constraint, like=False):
        """
        Looks for proteins that meet a given constraint on a specific hierarchical classification level. 
            
        arguments:
            level: a hierarchical classification level 
                
            constraint: a possible classification for the level
            
        return:
            a list of protein identifiers in the form of tuples (structure, chain).  
        """
        exec like and 'scopProteinData = Session.query(SCOPProteinData).filter(SCOPProteinData.%s.like("%s")).all()' % (level, '%' + constraint + '%') or 'scopProteinData = Session.query(SCOPProteinData).filter_by(%s=constraint).all()' % level
        str_ids = [ protein_data.str_id for protein_data in scopProteinData ]
        found_chains = [ (chain.str_id, chain.chain_id) for chain in Session.query(Chain).filter(Chain.str_id.in_(str_ids)).all() ]
        return self.__ids and [ protein_id for protein_id in self.__ids if protein_id in found_chains ] or found_chains

    def lookForClassification(self, **classification):
        """
        Looks for proteins that meet a given constraint on the SCOP classification.
        
        arguments:
           **classification: a SCOP classification (keys: 'Class', 'fold', 'family', 'superfamily'). 
            
        return:
            a list of protein identifiers in the form of tuples (structure, chain).
        """
        protein_ids = set(self.__ids)
        for (level, constraint) in classification.items():
            try:
                exec 'protein_ids&=set(self._SCOP__lookFor(level,constraint))'
            except:
                return []

        return list(protein_ids)