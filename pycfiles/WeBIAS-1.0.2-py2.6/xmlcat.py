# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/gnosis/xml/xmlcat.py
# Compiled at: 2015-04-13 16:10:50
import sys
from xml.sax import handler, make_parser
from xml.sax.saxutils import escape

class Canonicalize(handler.ContentHandler):

    def __init__(self, out=sys.stdout):
        handler.ContentHandler.__init__(self)
        self._out = out

    def startDocument(self):
        xml_decl = '<?xml version="1.0" encoding="utf-8"?>\n'
        self._out.write(xml_decl)

    def endDocument(self):
        pass

    def startElement(self, name, attrs):
        self._out.write('<' + name)
        name_val = attrs.items()
        name_val.sort()
        for (name, value) in name_val:
            self._out.write(' %s="%s"' % (name, escape(value)))

        self._out.write('>')

    def endElement(self, name):
        self._out.write('</%s>' % name)

    def characters(self, content):
        self._out.write(escape(content))

    def ignorableWhitespace(self, content):
        pass

    def processingInstruction(self, target, data):
        self._out.write('<?%s %s?>' % (target, data))


class TextDump(handler.ContentHandler):

    def __init__(self, out=sys.stdout):
        self._out = out
        self.last = ''
        self.skipping = 0

    def characters(self, content):
        if self.last.strip() or content.strip():
            if self.skipping:
                self._out.write('\n')
                self.skipping = 0
            self._out.write(escape(content))
        elif self.last == '\n' and content != '\n':
            self._out.write(content)
        else:
            self.skipping = 1
        self.last = content


if __name__ == '__main__':
    parser = make_parser()
    if sys.argv[1] in ('-dump', '--dump', '/dump'):
        del sys.argv[1]
        parser.setContentHandler(TextDump())
    else:
        parser.setContentHandler(Canonicalize())
    for fname in sys.argv[1:]:
        parser.parse(fname)