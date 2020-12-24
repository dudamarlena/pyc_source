# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Xml\Xvif.py
# Compiled at: 2006-01-15 22:59:42
"""
XVIF integration for 4Suite.  Includes basic RELAX NG support

Copyright 2006 Fourthought, Inc. (USA).
Detailed license and copyright information: http://4suite.org/COPYRIGHT
Project home, documentation, distributions: http://4suite.org/
"""
from xml.dom import Node
from Ft.Xml import InputSource, Sax
from Ft.Xml.Domlette import NonvalidatingReader, SaxWalker
from Ft.Xml.ThirdParty.Xvif import rng

class RelaxNgValidator:
    """
    A class providing RELAX NG support
    """
    __module__ = __name__

    def __init__(self, isrc_or_domlette):
        if isinstance(isrc_or_domlette, InputSource.InputSource):
            parser = Sax.CreateParser()
            self._schema = rng.RngParser()
            parser.setContentHandler(self._schema)
            parser.parse(isrc_or_domlette)
        elif isinstance(isrc_or_domlette, Node):
            parser = SaxWalker(isrc_or_domlette)
            self._schema = rng.RngParser()
            parser.setContentHandler(self._schema)
            parser.parse()
        else:
            raise TypeError('Expected InputSource or Domlette Document, got %s' % isrc_or_domlette)

    def isValid(self, isrc):
        reader = NonvalidatingReader
        doc = reader.parse(isrc)
        return self.isValidNode(doc.firstChild)

    def isValidNode(self, node):
        deriv = self.validateNode(node)
        isvalid = deriv.nullable()
        return isvalid

    def validate(self, isrc):
        reader = NonvalidatingReader
        doc = reader.parse(isrc)
        return self.validateNode(doc.firstChild)

    def validateNode(self, node):
        if node.nodeType == Node.DOCUMENT_NODE:
            node = node.firstChild
        return self._schema.grammar.deriv(node)


class RngInvalid(Exception):
    __module__ = __name__

    def __init__(self, rngResult):
        self.message = rngResult.msg
        Exception.__init__(self, self.message)