# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/pydataportability/microformats/base/parser.py
# Compiled at: 2008-04-19 15:06:13
from zope.component import queryUtility, getUtility, getUtilitiesFor
from zope.interface import implements
from interfaces import IMicroformatsParser, IHTMLNode

class MicroformatsParser(object):
    """parse an HTML documents for microformats and return a list"""
    __module__ = __name__
    implements(IMicroformatsParser)

    def __init__(self, node, parsers_to_use=[]):
        self.node = IHTMLNode(node)
        self.microformats = {}
        self.parsers = {}
        self.parsers_to_use = parsers_to_use
        self.initializeParsers()

    def initializeParsers(self):
        """retrieve the list of parsers"""
        parsers = getUtilitiesFor(IMicroformatsParser)
        for (name, parser) in parsers:
            if self.parsers_to_use != []:
                if name in self.parsers_to_use:
                    self.parsers[name] = parser()
            else:
                self.parsers[name] = parser()

    def parse(self):
        """parse the document"""
        for inode in self.node.getiterator():
            node = IHTMLNode(inode)
            for (name, parser) in self.parsers.items():
                if parser.checkNode(node):
                    results = parser.parseNode(node)
                    self.microformats.setdefault(name, []).append(results)