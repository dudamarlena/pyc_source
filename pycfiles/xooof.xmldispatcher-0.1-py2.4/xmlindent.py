# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xooof/xmldispatcher/tools/unittest/xmlindent.py
# Compiled at: 2008-10-01 10:39:34
import string, re, xml.sax
from xml.sax.saxutils import XMLGenerator

class XMLIndentGenerator(XMLGenerator):
    """ An XMLGenerator that indents but does not support mixed content

        If mixed content is detected, RuntimeError is raised.
    """
    __module__ = __name__

    def __init__(self, out, encoding='iso-8859-1'):
        XMLGenerator.__init__(self, out, encoding)
        self.__out = out
        self.__inElement = 0
        self.__indent = -1
        self.__characters = []

    def _flushCharacters(self, mustBeWS):
        chars = string.join(self.__characters, '')
        if mustBeWS:
            if not re.match('\\s*$', chars):
                raise RuntimeError("non whitespace detected (because of mixed content?): '%s'" % chars)
        else:
            XMLGenerator.characters(self, chars)
        self.__characters = []

    def characters(self, characters):
        self.__characters.append(characters)

    def _start(self):
        self._flushCharacters(1)
        self.__inElement = 1
        self.__indent += 1
        self.__out.write('\n')
        self.__out.write('  ' * self.__indent)

    def startElement(self, name, attrs):
        self._start()
        XMLGenerator.startElement(self, name, attrs)

    def startElementNS(self, name, qname, attrs):
        self._start()
        XMLGenerator.startElementNS(self, name, qname, attrs)

    def _end(self):
        self._flushCharacters(not self.__inElement)
        if not self.__inElement:
            self.__out.write('\n')
            self.__out.write('  ' * self.__indent)
        self.__indent -= 1
        self.__inElement = 0

    def endElement(self, name):
        self._end()
        XMLGenerator.endElement(self, name)

    def endElementNS(self, name, qname):
        self._end()
        XMLGenerator.endElementNS(self, name, qname)


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print >> sys.stderr, 'usage: %s <in file> <out file>' % sys.argv[0]
        sys.exit(1)
    if sys.argv[1] == '-':
        inf = sys.stdin
    else:
        inf = open(sys.argv[1])
    if sys.argv[2] == '-':
        outf = sys.stdout
    else:
        outf = open(sys.argv[2], 'w')
    xml.sax.parse(inf, XMLIndentGenerator(outf))
    outf.write('\n')