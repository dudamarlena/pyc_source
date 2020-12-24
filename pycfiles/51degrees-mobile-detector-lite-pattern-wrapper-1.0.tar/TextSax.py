# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\Xslt\TextSax.py
# Compiled at: 2001-12-26 22:53:48
__doc__ = '\nComponents for reading Text files from a SAX-like producer.\nWWW: http://4suite.org/4DOM         e-mail: support@4suite.org\n\nCopyright (c) 1999-2001 Fourthought Inc, USA.   All Rights Reserved.\nSee  http://4suite.org/COPYRIGHT  for license and copyright information\n'

class TextGenerator:
    __module__ = __name__

    def __init__(self, keepAllWs=0):
        self.__currText = ''
        self.__keepAllWs = keepAllWs

    def getRootNode(self):
        return self.__currText

    def startElement(self, name, attribs):
        st = '<' + name
        for attr in attribs.keys():
            st = st + ' %s = %s ' % (attr, attribs[attr])

        st = st + '>\n'
        self.__currText = self.__currText + st

    def endElement(self, name):
        st = '</%s>' % name
        self.__currText = self.__currText + st

    def ignorableWhitespace(self, ch, start, length):
        """
        If 'keepAllWs' permits, add ignorable white-space as a text node.
        Remember that a Document node cannot contain text nodes directly.
        If the white-space occurs outside the root element, there is no place
        for it in the DOM and it must be discarded.
        """
        if self.__keepAllWs:
            self.__currText = self.__currText + ch[start:start + length]

    def characters(self, ch, start, length):
        self.__currText = self.__currText + ch[start:start + length]

    def error(self, exception):
        raise exception

    def fatalError(self, exception):
        raise exception