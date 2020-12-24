# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Xml\Xslt\NumberElement.py
# Compiled at: 2005-04-06 18:05:47
"""
Implementation of xsl:number

Copyright 2003 Fourthought, Inc. (USA).
Detailed license and copyright information: http://4suite.org/COPYRIGHT
Project home, documentation, distributions: http://4suite.org/
"""
from Ft.Lib import number
from Ft.Xml import EMPTY_NAMESPACE
from Ft.Xml.Xslt import XsltElement, XSL_NAMESPACE
from Ft.Xml.Xslt import CategoryTypes, AttributeInfo, ContentInfo
from Ft.Xml.Xslt import XsltException, XsltRuntimeException, Error
from Ft.Xml.XPath import Conversions
from NumberFormatter import DefaultFormatter
DEFAULT_LANG = 'en'
DEFAULT_FORMAT = '1'
SINGLE = 0
MULTIPLE = 1
ANY = 2
SIMPLE = 3

class NumberElement(XsltElement):
    __module__ = __name__
    category = CategoryTypes.INSTRUCTION
    content = ContentInfo.Empty
    legalAttrs = {'level': AttributeInfo.Choice(['single', 'multiple', 'any'], default='single'), 'count': AttributeInfo.Pattern(), 'from': AttributeInfo.Pattern(), 'value': AttributeInfo.Expression(), 'format': AttributeInfo.StringAvt(default='1'), 'lang': AttributeInfo.NMToken(), 'letter-value': AttributeInfo.ChoiceAvt(['alphabetic', 'traditional']), 'grouping-separator': AttributeInfo.CharAvt(), 'grouping-size': AttributeInfo.NumberAvt(default=0)}
    doesSetup = 1

    def setup(self):
        if self._level == 'single':
            if not self._count and not self._from:
                self._level = SIMPLE
            else:
                self._level = SINGLE
        elif self._level == 'multiple':
            self._level = MULTIPLE
        elif self._level == 'any':
            self._level = ANY
        if self._format.isConstant():
            self._formatter = self.createFormatter(self._format.evaluate(None), language=self._lang)
        else:
            self._formatter = None
        return
        return

    def createFormatter(self, format, language=None, letterValue=None):
        """
        Creates a formatter appropriate for the given language and
        letterValue, or a default, English-based formatter. Raises an
        exception if the language or letterValue is unsupported.
        Currently, if the language value is given, it must indicate
        English.
        """
        if language and not language.lower().startswith('en'):
            raise XsltRuntimeException(Error.UNSUPPORTED_NUMBER_LANG_VALUE, self, language)
        if letterValue and letterValue != 'traditional':
            if not language or language.lower().startswith('en'):
                raise XsltRuntimeException(Error.UNSUPPORTED_NUMBER_LETTER_FOR_LANG, self, letterValue, language or 'en')
        return DefaultFormatter(format)

    def instantiate(self, context, processor):
        if self._value:
            value = Conversions.NumberValue(self._value.evaluate(context))
            if not number.finite(value) or value < 0.5:
                processor.writers[(-1)].text(Conversions.StringValue(value))
                return
            else:
                values = [
                 int(round(value))]
        else:
            node = context.node
            if self._level == SINGLE:
                value = self._single_value(context, node, self._count, self._from)
                if value == 0:
                    values = []
                else:
                    values = [
                     value]
            elif self._level == MULTIPLE:
                values = self._multiple_values(context, node)
            elif self._level == ANY:
                value = self._any_value(context, node)
                if value == 0:
                    values = []
                else:
                    values = [
                     value]
            else:
                value = 1
                prev = node.previousSibling
                type = node.nodeType
                expanded = (node.namespaceURI, node.localName)
                while prev:
                    if prev.nodeType == type and (prev.namespaceURI, prev.localName) == expanded:
                        value += 1
                    prev = prev.previousSibling

                values = [
                 value]
        grouping_size = int(self._grouping_size.evaluate(context))
        if grouping_size:
            grouping_separator = self._grouping_separator.evaluate(context)
        else:
            grouping_separator = None
        formatter = self._formatter
        if not formatter:
            format = self._format and self._format.evaluate(context) or DEFAULT_FORMAT
            lang = self._lang and self._lang.evaluate(context) or DEFAULT_LANG
            letter_value = self._letter_value.evaluate(context) or ''
            formatter = self.createFormatter(format, lang, letter_value)
        numstr = formatter.format(values, grouping_size, grouping_separator)
        processor.writers[(-1)].text(numstr)
        return
        return

    def _single_value(self, context, node, countPattern, fromPattern):
        if not countPattern:
            if not node.localName:
                countPattern = NodeTypeTest(node)
            else:
                countPattern = NameTest(node)
        if fromPattern:
            start = node.parentNode
            while start and not fromPattern.match(context, start):
                start = start.parentNode

        else:
            start = node.rootNode
        while not countPattern.match(context, node):
            node = node.parentNode
            if node is None or node == start:
                return 0

        value = 0
        while node:
            value += 1
            node = node.previousSibling
            while node and not countPattern.match(context, node):
                node = node.previousSibling

        return value
        return

    def _multiple_values(self, context, node):
        if not self._count:
            if not node.localName:
                count = NodeTypeTest(node)
            else:
                count = NameTest(node)
        else:
            count = self._count
        values = []
        while node:
            if count.match(context, node):
                value = self._single_value(context, node, count, None)
                values.insert(0, value)
            node = node.parentNode
            if node and self._from and self._from.match(context, node):
                break

        return values
        return

    def _any_value(self, context, node):
        if not self._count:
            if not node.localName:
                count = NodeTypeTest(node)
            else:
                count = NameTest(node)
        else:
            count = self._count
        value = 0
        while node:
            if self._from and self._from.match(context, node):
                break
            if count.match(context, node):
                value += 1
            if not node.previousSibling:
                node = node.parentNode
            else:
                node = node.previousSibling
                while node.lastChild:
                    node = node.lastChild

        return value


class NodeTypeTest:
    __module__ = __name__

    def __init__(self, node):
        self.nodeType = node.nodeType
        return

    def match(self, context, node):
        return node.nodeType == self.nodeType


class NameTest:
    __module__ = __name__

    def __init__(self, node):
        self.nodeType = node.nodeType
        self.localName = node.localName
        self.namespaceURI = node.namespaceURI
        return

    def match(self, context, node):
        return node.nodeType == self.nodeType and node.localName == self.localName and node.namespaceURI == self.namespaceURI