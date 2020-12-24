# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/suds/sax/parser.py
# Compiled at: 2010-01-12 12:39:45
"""
The sax module contains a collection of classes that provide a
(D)ocument (O)bject (M)odel representation of an XML document.
The goal is to provide an easy, intuative interface for managing XML
documents.  Although, the term, DOM, is used above, this model is
B{far} better.

XML namespaces in suds are represented using a (2) element tuple
containing the prefix and the URI.  Eg: I{('tns', 'http://myns')}

"""
from logging import getLogger
import suds.metrics
from suds import *
from suds.sax import *
from suds.sax.document import Document
from suds.sax.element import Element
from suds.sax.text import Text
from suds.sax.attribute import Attribute
from xml.sax import make_parser, InputSource, ContentHandler
from xml.sax.handler import feature_external_ges
from cStringIO import StringIO
log = getLogger(__name__)

class Handler(ContentHandler):
    """ sax hanlder """

    def __init__(self):
        self.nodes = [
         Document()]

    def startElement(self, name, attrs):
        top = self.top()
        node = Element(unicode(name), parent=top)
        for a in attrs.getNames():
            n = unicode(a)
            v = unicode(attrs.getValue(a))
            attribute = Attribute(n, v)
            if self.mapPrefix(node, attribute):
                continue
            node.append(attribute)

        node.charbuffer = []
        top.append(node)
        self.push(node)

    def mapPrefix(self, node, attribute):
        skip = False
        if attribute.name == 'xmlns':
            if len(attribute.value):
                node.expns = unicode(attribute.value)
            skip = True
        elif attribute.prefix == 'xmlns':
            prefix = attribute.name
            node.nsprefixes[prefix] = unicode(attribute.value)
            skip = True
        return skip

    def endElement(self, name):
        name = unicode(name)
        current = self.top()
        if len(current.charbuffer):
            current.text = Text(('').join(current.charbuffer))
        del current.charbuffer
        if len(current):
            current.trim()
        currentqname = current.qname()
        if name == currentqname:
            self.pop()
        else:
            raise Exception('malformed document')

    def characters(self, content):
        text = unicode(content)
        node = self.top()
        node.charbuffer.append(text)

    def push(self, node):
        self.nodes.append(node)
        return node

    def pop(self):
        return self.nodes.pop()

    def top(self):
        return self.nodes[(len(self.nodes) - 1)]


class Parser:
    """ SAX Parser """

    @classmethod
    def saxparser(cls):
        p = make_parser()
        p.setFeature(feature_external_ges, 0)
        h = Handler()
        p.setContentHandler(h)
        return (p, h)

    def parse(self, file=None, string=None):
        """
        SAX parse XML text.
        @param file: Parse a python I{file-like} object.
        @type file: I{file-like} object.
        @param string: Parse string XML.
        @type string: str
        """
        timer = metrics.Timer()
        timer.start()
        (sax, handler) = self.saxparser()
        if file is not None:
            sax.parse(file)
            timer.stop()
            metrics.log.debug('sax (%s) duration: %s', file, timer)
            return handler.nodes[0]
        else:
            if string is not None:
                source = InputSource(None)
                source.setByteStream(StringIO(string))
                sax.parse(source)
                timer.stop()
                metrics.log.debug('%s\nsax duration: %s', string, timer)
                return handler.nodes[0]
            return