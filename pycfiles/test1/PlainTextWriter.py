# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Xml\Xslt\PlainTextWriter.py
# Compiled at: 2005-02-09 03:57:09
"""
Plain text writer for XSLT processor output

Copyright 2005 Fourthought, Inc. (USA).
Detailed license and copyright information: http://4suite.org/COPYRIGHT
Project home, documentation, distributions: http://4suite.org/
"""
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