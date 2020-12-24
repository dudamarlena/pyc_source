# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Xml\Xslt\StringWriter.py
# Compiled at: 2005-02-09 03:57:09
"""
A specialized XSLT output writer that only captures text output events

Copyright 2005 Fourthought, Inc. (USA).
Detailed license and copyright information: http://4suite.org/COPYRIGHT
Project home, documentation, distributions: http://4suite.org/
"""
import NullWriter

class StringWriter(NullWriter.NullWriter):
    __module__ = __name__

    def __init__(self, outputParams):
        NullWriter.NullWriter.__init__(self, outputParams)
        self._result = []
        self._ignore_events = 0
        self.had_nontext = False

    def getResult(self):
        return ('').join(self._result)

    def text(self, text, escapeOutput=True):
        if not self._ignore_events:
            self._result.append(text)
        return

    def startElement(self, name, namespace=None, extraNss=None):
        self._ignore_events += 1
        self.had_nontext = True
        return

    def endElement(self, name, namespace=None):
        self._ignore_events -= 1
        return

    def comment(self, body):
        self.had_nontext = True
        return

    def processingInstruction(self, target, data):
        self.had_nontext = True
        return

    def attribute(self, name, value, namespace=None):
        self.had_nontext = True
        return