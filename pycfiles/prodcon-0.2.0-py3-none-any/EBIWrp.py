# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/ProDaMa/EBIWrp.py
# Compiled at: 2009-10-09 05:50:00
__doc__ = '\nA wrapper for the EBI web server, to retrieve information about CATH and SCOP classified proteins.\n'
from ProDaMa.model.dbSession import *
import httplib

class EBIWrp(object):
    """
    Retrieves information about SCOP classified proteins.
    """

    def __remove_tags(self, line):
        """
        Removes html/xml tags from an input string.
        """
        while '<' in line:
            start = line.rfind('<')
            end = line.rfind('>')
            line = line[:start] + line[end + 1:]

        return line

    def __isRelevant(self, line):
        """
        Checks if the given string contains information relevant with the CATH or SCOP protein classification.
        
        return:
            a boolean value. Returns True if the line contains information about the classification, else returns False
        """
        return line and not line.isspace() and len([ line_part for line_part in line.split(' ') if line_part ]) > 1

    def __httpResponseFilter(self, response):
        """
        Reads the HTTP response and filters it keeping the data related to the protein CATH or SCOP classification.
        """
        start = response.rfind('<table class="content_table">')
        end = response.rfind('<table class="footerpane"')
        response = response[start:end]
        return [ line for line in [ self.__remove_tags(i) for i in response.replace('\n', '').replace('  ', '').split('</tr>') ] if self.__isRelevant(line) ]

    def __getClassification(self, url):
        """
        Gets the page related to the given URL (SCOP and CATH EBI retrieval pages) and reads the relevant data.
        """
        httpConnection = httplib.HTTPConnection('www.ebi.ac.uk')
        httpConnection.request('GET', url)
        response = httpConnection.getresponse()
        if response.status == 200:
            response = response.read()
        else:
            raise httplib.HTTPException()
        response = self.__httpResponseFilter(response)[1:]
        protein_classification = {}
        for data in response:
            levels = [ level.strip() for level in data.split('   ') if level ]
            protein_classification[levels[0]] = (' ').join(levels[1:])

        return protein_classification

    def getSCOPClassification(self, str_id):
        """
        Given a structure identifier retrieves a SCOP classification.

        parameters:
            str_id: a structure protein identifier

        return:
            if the protein is SCOP classified returns a SCOPProteinData object, else returns None
        """
        try:
            return self.__getClassification('/pdbe-srv/view/entry/%s/refscop' % str_id.lower())
        except:
            return

        return

    def getCATHClassification(self, str_id):
        """
        Given a structure identifier retrieves a CATH classification.

        parameters:
            str_id: a structure protein identifier

        return:
            if the protein is CATH classified returns a CATHProteinData object, else returns None
        """
        try:
            return self.__getClassification('/pdbe-srv/view/entry/%s/refcath' % str_id.lower())
        except:
            return

        return