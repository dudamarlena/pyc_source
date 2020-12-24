# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/io/UrlOps.py
# Compiled at: 2019-12-11 16:37:52
"""Provide tools for handling downloading data from urls."""
import urllib2, socket
from logging import Logger
from hashlib import sha256

class HashError(Exception):
    """Thrown when a checksum check fails"""

    def __init__(self, sData):
        super(HashError, self).__init__('Checksum comparison failed')
        self.sData = sData


def urlopen_with_timeout(sUrl, fErrorHandler=None, dHeaders=None, sData=None):
    """Wrap urllib2.urlopen to handle timeouts nicely"""
    oReq = urllib2.Request(sUrl)
    if dHeaders:
        for sHeader, sValue in dHeaders.items():
            oReq.add_header(sHeader, sValue)

    if sData:
        oReq.add_data(sData)
    try:
        return urllib2.urlopen(oReq)
    except urllib2.URLError as oExp:
        if fErrorHandler:
            fErrorHandler(oExp)
        else:
            raise
    except socket.timeout as oExp:
        if fErrorHandler:
            fErrorHandler(oExp)
        else:
            raise

    return


def fetch_data(oFile, oOutFile=None, sHash=None, oLogHandler=None, fErrorHandler=None):
    """Fetch data from a file'ish object (EncodedFile, urlopen or file)"""
    try:
        if hasattr(oFile, 'info') and callable(oFile.info):
            sLength = oFile.info().getheader('Content-Length')
        else:
            sLength = None
        if sLength:
            oLogger = Logger('Sutekh data fetcher')
            if oLogHandler is not None:
                oLogger.addHandler(oLogHandler)
            aData = []
            iLength = int(sLength)
            if hasattr(oLogHandler, 'set_total'):
                oLogHandler.set_total((iLength + 9999) // 10000)
            iTotal = 0
            bCont = True
            while bCont:
                sInf = oFile.read(10000)
                iTotal += len(sInf)
                if sInf:
                    oLogger.info('%d downloaded', iTotal)
                    if oOutFile:
                        oOutFile.write(sInf)
                    else:
                        aData.append(sInf)
                else:
                    bCont = False

            if oOutFile:
                sData = None
            else:
                sData = ('').join(aData)
        elif oOutFile:
            oOutFile.write(oFile.read())
            sData = None
        else:
            sData = oFile.read()
    except urllib2.URLError as oExp:
        if fErrorHandler:
            fErrorHandler(oExp)
            sData = None
        else:
            raise
    except socket.timeout as oExp:
        if fErrorHandler:
            fErrorHandler(oExp)
            sData = None
        else:
            raise

    if sHash is not None:
        if sData is not None:
            sDataHash = sha256(sData).hexdigest()
            if sDataHash != sHash:
                raise HashError(sData)
    return sData