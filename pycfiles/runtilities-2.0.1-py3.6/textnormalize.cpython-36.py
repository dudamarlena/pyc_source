# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\running\textnormalize.py
# Compiled at: 2009-10-11 16:36:28
# Size of source mod 2**32: 2294 bytes
from xml.sax.saxutils import XMLFilterBase

class text_normalize_filter(XMLFilterBase):
    __doc__ = '\n    SAX filter to ensure that contiguous white space nodes are\n    delivered merged into a single node\n    '

    def __init__(self, upstream, downstream):
        XMLFilterBase.__init__(self, upstream)
        self._downstream = downstream
        self._accumulator = []

    def _complete_text_node(self):
        if self._accumulator:
            self._downstream.characters(''.join(self._accumulator))
            self._accumulator = []

    def startElement(self, name, attrs):
        self._complete_text_node()
        self._downstream.startElement(name, attrs)

    def startElementNS(self, name, qname, attrs):
        self._complete_text_node()
        self._downstream.startElementNS(name, qname, attrs)

    def endElement(self, name):
        self._complete_text_node()
        self._downstream.endElement(name)

    def endElementNS(self, name, qname):
        self._complete_text_node()
        self._downstream.endElementNS(name, qname)

    def processingInstruction(self, target, body):
        self._complete_text_node()
        self._downstream.processingInstruction(target, body)

    def comment(self, body):
        self._complete_text_node()
        self._downstream.comment(body)

    def characters(self, text):
        self._accumulator.append(text)

    def ignorableWhitespace(self, ws):
        self._accumulator.append(text)


if __name__ == '__main__':
    import sys
    from xml import sax
    from xml.sax.saxutils import XMLGenerator
    parser = sax.make_parser()
    downstream_handler = XMLGenerator()
    filter_handler = text_normalize_filter(parser, downstream_handler)
    filter_handler.parse(sys.argv[1])