# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/entify/lib/config_entify.py
# Compiled at: 2015-01-05 13:39:33
import os, copy, logging
from entify.lib.patterns.bitcoinaddress import BitcoinAddress
from entify.lib.patterns.dni import DNI
from entify.lib.patterns.dogecoinaddress import DogecoinAddress
from entify.lib.patterns.email import Email
from entify.lib.patterns.ipv4 import IPv4
from entify.lib.patterns.litecoinaddress import LitecoinAddress
from entify.lib.patterns.md5 import MD5
from entify.lib.patterns.namecoinaddress import NamecoinAddress
from entify.lib.patterns.peercoinaddress import PeercoinAddress
from entify.lib.patterns.sha1 import SHA1
from entify.lib.patterns.sha256 import SHA256
from entify.lib.patterns.url import URL

def getAllRegexp():
    """ 
        Method that recovers ALL the list of <RegexpObject> classes to be processed....

        :return:    Returns a list [] of <RegexpObject> classes.
    """
    logger = logging.getLogger('entify')
    logger.debug('Recovering all the available <RegexpObject> classes.')
    listAll = []
    listAll.append(BitcoinAddress())
    listAll.append(DNI())
    listAll.append(DogecoinAddress())
    listAll.append(Email())
    listAll.append(IPv4())
    listAll.append(LitecoinAddress())
    listAll.append(MD5())
    listAll.append(NamecoinAddress())
    listAll.append(PeercoinAddress())
    listAll.append(SHA1())
    listAll.append(SHA256())
    listAll.append(URL())
    logger.debug('Returning a list of ' + str(len(listAll)) + ' <RegexpObject> classes.')
    return listAll


def getAllRegexpNames(regexpList=None):
    """ 
        Method that recovers the names of the <RegexpObject> in a given list.

        :param regexpList:    list of <RegexpObject>. If None, all the available <RegexpObject> will be recovered.

        :return:    Array of strings containing the available regexps.
    """
    if regexpList == None:
        regexpList = getAllRegexp()
    listNames = [
     'all']
    for r in regexpList:
        listNames.append(r.name)

    return listNames


def getRegexpsByName(regexpNames=[
 'all']):
    """ 
        Method that recovers the names of the <RegexpObject> in a given list.

        :param regexpNames:    list of strings containing the possible regexp.

        :return:    Array of <RegexpObject> classes.
    """
    allRegexpList = getAllRegexp()
    if 'all' in regexpNames:
        return allRegexpList
    regexpList = []
    for name in regexpNames:
        for r in allRegexpList:
            if name == r.name:
                regexpList.append(r)

    return regexpList