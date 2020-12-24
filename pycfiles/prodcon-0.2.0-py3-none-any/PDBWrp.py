# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/ProDaMa/PDBWrp.py
# Compiled at: 2009-10-06 08:42:18
import datetime, cPickle
from ftplib import FTP
from ProDaMa.services.config import *
from ProDaMa.services.PDBClient import PDBClient
from ProDaMa.services.serviceExceptions import SOAPException

class PDBWrp(object):
    """
   Retrieves information about a protein from PDB.
 """

    def __init__(self):
        """
    Initializes the SOAP client.
    """
        self.__client = PDBClient()

    def getSequence(self, str_id, chain_id):
        """
     Retrieves the amino acids sequence of a protein.

    required:
        str_id : a stucture protein identifier
        chain_id : a chain ideintifier
    
    return:
        a string
    """
        try:
            return self.__client.getSequenceForStructureAndChain(str_id, chain_id)
        except Exception:
            raise SOAPException()

    def getStructure(self, str_id, chain_id):
        """
    Retrieves the secondary structure of a protein.

    required:
        str_id : a stucture protein identifier
        chain_id : a chain ideintifier

    return:
        a string
    """
        try:
            return self.__client.getKabschSander(str_id, chain_id)
        except Exception:
            raise SOAPException()

    def getIds(self):
        """
    Retrieves all PDB structures identifiers.

    return:
        a list of protein structure identifiers (without the chain identifier)
    
    """
        return self.__client.getCurrentPdbIds()

    def getObsoleteIds(self):
        """
    Retrieves all obsolete PDB protein identifiers.

    return:
        a list of protein structure identifiers (without the chain identifier)
    """
        return self.__client.getObsoletePdbIds()

    def getChains(self, str_id):
        """
    Given a protein structure identifier retrieves its chain identifiers.

    required:
        str_id: a structure protein identifier
    
    return:
        a list of chain identifiers
    """
        return self.__client.getChains(str_id)

    def lookForChanges(self):
        """
        Looks for changes in PDB files.

        return:
            a list of protein structure identifiers
        """
        ftp = FTP('ftp.wwpdb.org')
        ftp.login()
        ftp.cwd('/pub/pdb/data/status')
        ftp_dir = []
        ftp.retrlines('LIST', ftp_dir.append)
        ftp_dates = [ datetime.date(int(i.split(' ')[(-1)][:4]), int(i.split(' ')[(-1)][4:6]), int(i.split(' ')[(-1)][6:])) for i in ftp_dir[:-1]
                    ]
        last = self.__getLastUpdate()
        modified = []
        for ftp_date in [ str(ftp_date).replace('-', '') for ftp_date in ftp_dates if ftp_date > last ]:
            ftp.cwd('/pub/pdb/data/status/%s' % ftp_date)
            ftp.retrlines('RETR modified.nmr', modified.append)

        self.__setLastUpdate()
        return [ str_id.upper() for str_id in modified ]

    def __getLastUpdate(self):
        """
        Gets the date of the last time has been updated the local database.
        """
        try:
            date_file = open(DATA + '/last_update', 'r')
            date = cPickle.load(date_file)
            date_file.close()
        except:
            date = datetime.date.min

        return date

    def __setLastUpdate(self):
        """
        Stores in a local file the date of the last time the local database has been updated.
        """
        date_file = open(DATA + '/last_update', 'w')
        cPickle.dump(datetime.date.today(), date_file)
        date_file.close()