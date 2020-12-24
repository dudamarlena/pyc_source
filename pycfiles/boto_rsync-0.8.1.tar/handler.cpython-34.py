# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/handler.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 2382 bytes
import xml.sax
from boto.compat import StringIO

class XmlHandler(xml.sax.ContentHandler):

    def __init__(self, root_node, connection):
        self.connection = connection
        self.nodes = [('root', root_node)]
        self.current_text = ''

    def startElement(self, name, attrs):
        self.current_text = ''
        new_node = self.nodes[(-1)][1].startElement(name, attrs, self.connection)
        if new_node is not None:
            self.nodes.append((name, new_node))

    def endElement(self, name):
        self.nodes[(-1)][1].endElement(name, self.current_text, self.connection)
        if self.nodes[(-1)][0] == name:
            if hasattr(self.nodes[(-1)][1], 'endNode'):
                self.nodes[(-1)][1].endNode(self.connection)
            self.nodes.pop()
        self.current_text = ''

    def characters(self, content):
        self.current_text += content


class XmlHandlerWrapper(object):

    def __init__(self, root_node, connection):
        self.handler = XmlHandler(root_node, connection)
        self.parser = xml.sax.make_parser()
        self.parser.setContentHandler(self.handler)
        self.parser.setFeature(xml.sax.handler.feature_external_ges, 0)

    def parseString(self, content):
        return self.parser.parse(StringIO(content))