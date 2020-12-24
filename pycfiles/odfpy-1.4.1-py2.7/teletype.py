# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/odf/teletype.py
# Compiled at: 2020-01-18 11:47:38
"""
Class for handling whitespace properly in OpenDocument.

While it is possible to use getTextContent() and setTextContent()
to extract or create ODF content, these won't extract or create
the appropriate <text:s>, <text:tab>, or <text:line-break>
elements.  This module takes care of that problem.
"""
from odf.element import Node
import odf.opendocument
from odf.text import S, LineBreak, Tab

class WhitespaceText(object):

    def __init__(self):
        self.textBuffer = []
        self.spaceCount = 0

    def addTextToElement(self, odfElement, s):
        """ Process an input string, inserting
            <text:tab> elements for '   ',
            <text:line-break> elements for '
', and
            <text:s> elements for runs of more than one blank.
            These will be added to the given element.
        """
        i = 0
        ch = ' '
        while i < len(s):
            ch = s[i]
            if ch == '\t':
                self._emitTextBuffer(odfElement)
                odfElement.addElement(Tab())
                i += 1
            elif ch == '\n':
                self._emitTextBuffer(odfElement)
                odfElement.addElement(LineBreak())
                i += 1
            elif ch == ' ':
                self.textBuffer.append(' ')
                i += 1
                self.spaceCount = 0
                while i < len(s) and s[i] == ' ':
                    self.spaceCount += 1
                    i += 1

                if self.spaceCount > 0:
                    self._emitTextBuffer(odfElement)
                    self._emitSpaces(odfElement)
            else:
                self.textBuffer.append(ch)
                i += 1

        self._emitTextBuffer(odfElement)

    def _emitTextBuffer(self, odfElement):
        """ Creates a Text Node whose contents are the current textBuffer.
            Side effect: clears the text buffer.
        """
        if len(self.textBuffer) > 0:
            odfElement.addText(('').join(self.textBuffer))
        self.textBuffer = []

    def _emitSpaces(self, odfElement):
        """ Creates a <text:s> element for the current spaceCount.
            Side effect: sets spaceCount back to zero
        """
        if self.spaceCount > 0:
            spaceElement = S(c=self.spaceCount)
            odfElement.addElement(spaceElement)
        self.spaceCount = 0


def addTextToElement(odfElement, s):
    wst = WhitespaceText()
    wst.addTextToElement(odfElement, s)


def extractText(odfElement):
    """ Extract text content from an Element, with whitespace represented
        properly. Returns the text, with tabs, spaces, and newlines
        correctly evaluated. This method recursively descends through the
        children of the given element, accumulating text and "unwrapping"
        <text:s>, <text:tab>, and <text:line-break> elements along the way.
    """
    result = []
    if len(odfElement.childNodes) != 0:
        for child in odfElement.childNodes:
            if child.nodeType == Node.TEXT_NODE:
                result.append(child.data)
            elif child.nodeType == Node.ELEMENT_NODE:
                subElement = child
                tagName = subElement.qname
                if tagName == ('urn:oasis:names:tc:opendocument:xmlns:text:1.0', 'line-break'):
                    result.append('\n')
                elif tagName == ('urn:oasis:names:tc:opendocument:xmlns:text:1.0',
                                 'tab'):
                    result.append('\t')
                elif tagName == ('urn:oasis:names:tc:opendocument:xmlns:text:1.0',
                                 's'):
                    c = subElement.getAttribute('c')
                    if c:
                        spaceCount = int(c)
                    else:
                        spaceCount = 1
                    result.append(' ' * spaceCount)
                else:
                    result.append(extractText(subElement))

    return ('').join(result)