# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/ProDaMa/services/PDBClient.py
# Compiled at: 2009-10-07 09:12:16
__doc__ = '\nDefines the clients related to the used Protein Data Bank web services.\n'
from suds.client import Client
from serviceExceptions import SOAPException
from soaplib.client import make_service_client
from soaplib.service import soapmethod
from soaplib.wsgi_soap import SimpleWSGISoapApp
from soaplib.serializers.primitive import String

class KSPDBService(SimpleWSGISoapApp):

    @soapmethod(String, String, _returns=String, _outVariableName='getKabschSanderReturn')
    def getKabschSander(self, pdbid, chainID):
        pass


class PDBClient(object):
    """
    This class defines the clients used for invoking the PDB web services.
    """

    def __init__(self):
        self.client = Client('http://www.pdb.org/pdb/services/pdbws?wsdl')

    def fastaQuery(self, sequence, ecutoff):
        """
        Performs a FASTA query.
        
        arguments:
            sequence: a target sequence
            
            ecutoff: the E-value
            
        return:
            the FASTA response
        """
        try:
            return self.client.service.fastaQuery(sequence, ecutoff).fastaQueryReturn
        except:
            raise SOAPException

    def getSequenceForStructureAndChain(self, str_id, chain_id):
        """
        Retrieves the amino acidic sequence for a given chain.
        
        arguments:
            str_id: a protein structure identifier
            
            chain_id: a chain identifier
            
        return:
            the primary sequence
        
        """
        try:
            return str(self.client.service.getSequenceForStructureAndChain(str_id, chain_id))
        except:
            raise SOAPException

    def getKabschSander(self, str_id, chain_id):
        """
        Retrieves the secondary structure for a given chain.
        
        arguments:
            str_id: a protein structure identifier
            
            chain_id: a chain identifier
            
        return:
            the secondary structure
        """
        try:
            return make_service_client('http://www.pdb.org/pdb/services/pdbws', KSPDBService()).getKabschSander(str_id, chain_id)
        except:
            raise SOAPException

    def getChains(self, str_id):
        """
        Retrieves the chain identifiers for a given structure.
        
        arguments:
            str_id: a protein structure identifier
            
        returns:
            the chain identifiers
        """
        try:
            return self.client.service.getChains(str_id).getChainsReturn
        except:
            raise SOAPException

    def getObsoletePdbIds(self):
        """
        Retrieves the protein identifiers of the obsolete structures
        
        return:
            the protein identifiers
        """
        try:
            return self.client.service.getObsoletePdbIds().getObsoletePdbIdsReturn
        except:
            raise SOAPException

    def getCurrentPdbIds(self):
        """
        Retrieves the PDB Identifiers (aka PDB IDs) that are "current" structures - not obsolete, models, etc.
        """
        try:
            return self.client.service.getCurrentPdbIds().getCurrentPdbIdsReturn
        except:
            raise SOAPException