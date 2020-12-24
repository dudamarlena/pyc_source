# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/io/EncodedFile.py
# Compiled at: 2019-12-11 16:37:52
"""Tools for dealing with unopened files that follow the White Wolf encoding
   conventions."""
import codecs, urllib2, logging

def guess_encoding(sData, sFile):
    """Try to determine the correct encoding from the data"""
    aEncodings = [
     'utf8', 'iso8859-1']
    for sEnc in aEncodings:
        try:
            logging.info('Trying %s for %s', sEnc, sFile)
            sData.decode(sEnc)
            return sEnc
        except UnicodeDecodeError:
            pass

    raise RuntimeError('Unable to indentify correct encoding for %s' % sFile)


class EncodedFile(object):
    """EncodedFile is a convenience class which has an .open(..) method which
       returns a file-like object with the encoding set correctly.
       """

    def __init__(self, sfFile, bUrl=False, bFileObj=False):
        self.sfFile = sfFile
        self.bUrl = bUrl
        self.bFileObj = bFileObj
        if bUrl and bFileObj:
            raise ValueError('EncodedFile cannot be both a URL and a fileobject')

    def open(self):
        """Return a file object for the file.

           This expects a utf8 encoded file (possibly with BOM) and
           returns a file object producing utf8 strings."""
        if self.bFileObj:
            return self.sfFile
        if self.bUrl:
            oFile = urllib2.urlopen(self.sfFile)
            sData = oFile.read(1000)
            sFileEnc = guess_encoding(sData, self.sfFile)
            oFile.close()
            return codecs.EncodedFile(urllib2.urlopen(self.sfFile), 'utf8', sFileEnc)
        oFile = open(self.sfFile, 'rU')
        sData = oFile.read(1000)
        sFileEnc = guess_encoding(sData, self.sfFile)
        oFile.close()
        return codecs.EncodedFile(open(self.sfFile, 'rU'), 'utf8', sFileEnc)