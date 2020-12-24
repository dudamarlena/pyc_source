# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ProDaMa/MembraneProtein.py
# Compiled at: 2009-10-06 08:41:37
"""
To search for membrane proteins.
"""
from ProDaMa.model.dbSession import *

class MembraneProtein(object):
    """
    This class provides methods for analysing and searching for membrane proteins in the local database according to a given constraint. 
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

    def lookForMP(self, disposition=None):
        """
        Looks for membrane proteins (MP). If a disposition value is specified looks for MP that meet this constraint.

        arguments:
            disposition: a possible disposition value ('Transmembrane' or 'TM Monotopic')

        return:
            a list of protein identifiers in the form of tuples (structure, chain).
        """
        mpData = {True: Session.query(MPData), False: Session.query(MPData).filter_by(disposition=disposition)}[(disposition == None)].all()
        return self.__ids and [ (mp.str_id, mp.chain_id) for mp in mpData if (mp.str_id, mp.chain_id) in self.__ids ] or [ (mp.str_id, mp.chain_id) for mp in mpData ]

    def lookForTMSegments(self, **range):
        """
        Looks for transmembrane proteins (TM) with a number of TM segments smaller than a minimum value or bigger than a maximum value.  If minimum and maximum values are provided it looks for TM proteins with a number of TM segments between an lower and an upper limit.  
        
        arguments:
            **range: keys 'MIN' and 'MAX'

        return:
            a list of protein identifiers in the form of tuples (structure, chain).
        """
        mpData = {False: self.__ids and [ mp for mp in Session.query(MPData).all() if (mp.str_id, mp.chain_id) in self.__ids ], True: Session.query(MPData).all()}[(self.__ids == None)]
        if range.has_key('MIN'):
            mpData = [ mp for mp in mpData if int(mp.nb_segments) >= range['MIN'] ]
        if range.has_key('MAX'):
            mpData = [ mp for mp in mpData if int(mp.nb_segments) <= range['MAX'] ]
        return [ (mp.str_id, mp.chain_id) for mp in mpData ]

    def lookForTMTopology(self, topology=None):
        """
        Looks for transmembrane proteins (TM) that meet a given constraint on their topology.

        arguments:
            topology: a possible TM topology ('alpha helical' or 'beta barrel')

        return:
            a list of protein identifiers in the form of tuples (structure, chain).
        """
        mpData = {True: Session.query(MPData), False: Session.query(MPData).filter_by(topology=topology)}[(topology == None)].all()
        return self.__ids and [ (mp.str_id, mp.chain_id) for mp in mpData if (mp.str_id, mp.chain_id) in self.__ids ] or [ (mp.str_id, mp.chain_id) for mp in mpData ]