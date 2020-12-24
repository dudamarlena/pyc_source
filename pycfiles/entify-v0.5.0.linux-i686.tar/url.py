# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/entify/lib/patterns/url.py
# Compiled at: 2015-01-05 13:39:33
import re
from entify.lib.patterns.regexp import RegexpObject

class URL(RegexpObject):
    """ 
        <URL> class.
    """

    def __init__(self):
        """ 
            Constructor without parameters.
            Most of the times, this will be the ONLY method needed to be overwritten.

            :param name:    string containing the name of the regular expression.
            :param reg_exp:    string containing the regular expresion.
        """
        self.name = 'i3visio.url'
        self.reg_exp = [
         '((?:https?|s?ftp|file)://[a-zA-Z0-9\\_\\.\\-]+(?:\\:[0-9]{1,5}|)(?:/[a-zA-Z0-9\\_\\.\\-/=\\?&]+|))']

    def getAttributes(self, foundExp):
        """
            Method to extract additional attributes from a given expression (i. e.: domains and ports from URL and so on). This method may be overwritten in certain child classes.
            :param found_exp:   expression to be processed.
            :return:    The output format will be like:
                [{"type" : "i3visio.domain", "value": "twitter.com", "attributes": [] }, {"type" : "i3visio.protocol", "value": "http", "attributes": [] }]
        """
        attributes = []
        protocolRegExp = '((?:https?|s?ftp|file))://'
        foundProtocol = re.findall(protocolRegExp, foundExp)
        if len(foundProtocol) > 0:
            aux = {}
            aux['type'] = 'i3visio.protocol'
            aux['value'] = foundProtocol[0]
            aux['attributes'] = []
            attributes.append(aux)
        domainRegExp = '(?:https?|s?ftp)://([a-zA-Z0-9\\_\\.\\-]+)(?:\\:|/)'
        foundDomain = re.findall(domainRegExp, foundExp)
        if len(foundDomain) > 0:
            aux = {}
            aux['type'] = 'i3visio.domain'
            aux['value'] = foundDomain[0]
            aux['attributes'] = []
            attributes.append(aux)
        portRegExp = '(?:https?|s?ftp)://[a-zA-Z0-9\\_\\.\\-]+:([0-9]{1,5})/'
        foundPort = re.findall(portRegExp, foundExp)
        if len(foundPort) > 0:
            aux = {}
            aux['type'] = 'i3visio.port'
            aux['value'] = foundPort[0]
            aux['attributes'] = []
            attributes.append(aux)
        return attributes