# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\Xslt\PlainTextWriter.py
# Compiled at: 2005-02-09 03:57:09
__doc__ = '\nPlain text writer for XSLT processor output\n\nCopyright 2005 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
import codecs
from Ft.Xml.Xslt import NullWriter

class PlainTextWriter(NullWriter.NullWriter):
    __module__ = __name__

    def __init__(self, outputParams, stream):
        NullWriter.NullWriter.__init__(self, outputParams)
        self._outputParams.setDefault('mediaType', 'text/plain')
        self._outputParams.setDefault('encoding', 'utf-8')
        self._stream = codecs.lookup(self._outputParams.encoding)[3](stream)
        return

    def getStream(self):
        return self._stream.stream

    def text(self, text, escapeOutput=True):
        self._stream.write(text)
        return