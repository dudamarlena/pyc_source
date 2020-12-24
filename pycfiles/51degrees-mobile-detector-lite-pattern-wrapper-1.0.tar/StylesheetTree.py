# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\Xslt\StylesheetTree.py
# Compiled at: 2005-05-11 11:11:05
__doc__ = '\nNode classes for the stylesheet tree\n\nCopyright 2004 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
from Ft.Xml import EMPTY_NAMESPACE
from Ft.Xml.Domlette import GetAllNs
from Ft.Xml.Xslt import XSL_NAMESPACE, XsltException, XsltRuntimeException, Error
from Ft.Xml.Xslt import AttributeValueTemplate
from Ft.Xml.Xslt import CategoryTypes
from Ft.Xml.Xslt import ContentInfo
from Ft.Xml.XPath import parser
_xpath_parser = parser
from Ft.Xml.Xslt import parser
_xpattern_parser = parser
del parser

class XsltNode:
    __module__ = __name__
    baseUri = ''
    lineNumber = '??'
    columnNumber = '??'
    importIndex = -1
    root = None
    parent = None
    expandedName = (None, None)
    nodeName = None
    children = None
    attributes = None
    doesSetup = False
    doesPrime = False
    doesIdle = False

    def isLastChild(self):
        siblings = self.parent.children
        if siblings.index(self) == len(siblings) - 1:
            return 1
        else:
            isLast = 1
            for node in siblings[siblings.index(self) + 1:]:
                if not node.isPseudoNode():
                    isLast = 0
                    break

            return isLast

    def setup(self):
        return

    def prime(self, processor, context):
        return

    def idle(self, processor):
        return

    def instantiate(self, context, processor):
        return

    def isPseudoNode(self):
        return False

    def pprint(self, _indent=''):
        print _indent + str(self)
        if self.children:
            _indent += '  '
            for child in self.children:
                child.pprint(_indent)

        return


class XsltRoot(XsltNode):
    __module__ = __name__
    content = ContentInfo.Alt(ContentInfo.QName(XSL_NAMESPACE, 'xsl:stylesheet'), ContentInfo.QName(XSL_NAMESPACE, 'xsl:transform'), ContentInfo.ResultElements)
    validator = ContentInfo.Validator(content)
    nodeName = '#document'

    def __init__(self, baseUri):
        self.root = self
        self.baseUri = baseUri
        self.sources = {}
        self.sourceNodes = {}
        self.primeInstructions = []
        self.idleInstructions = []
        self.stylesheet = None
        self.children = []
        return
        return

    def appendChild(self, child):
        child.parent = self
        self.stylesheet = child
        self.children = [child]
        return

    def __str__(self):
        return '<XsltRoot at 0x%x>' % id(self)


class XsltElement(XsltNode):
    __module__ = __name__
    category = CategoryTypes.RESULT_ELEMENT
    content = ContentInfo.Template
    validator = ContentInfo.Validator(content)
    legalAttrs = None

    def __init__(self, root, namespaceUri, localName, baseUri):
        self.root = root
        self.baseUri = baseUri
        self.expandedName = (namespaceUri, localName)
        self.children = []
        self.attributes = {}
        self.namespaces = {}
        return

    def insertChild(self, index, child):
        """INTERNAL USE ONLY"""
        self.children.insert(index, child)
        child.parent = self
        if child.doesSetup:
            child.setup()
        return

    def appendChild(self, child):
        """INTERNAL USE ONLY"""
        self.children.append(child)
        child.parent = self
        if child.doesSetup:
            child.setup()
        return

    def parseAVT(self, avt):
        """DEPRECATED: specify an attribute in 'legalAttrs' instead."""
        if avt is None:
            return None
        try:
            return AttributeValueTemplate.AttributeValueTemplate(avt)
        except SyntaxError, error:
            raise XsltException(Error.INVALID_AVT, avt, self.baseUri, self.lineNumber, self.columnNumber, str(error))
        except XsltException, error:
            raise XsltException(Error.INVALID_AVT, avt, self.baseUri, self.lineNumber, self.columnNumber, error.args[0])

        return

    def parseExpression(self, expression):
        """DEPRECATED: specify an attribute in 'legalAttrs' instead."""
        if expression is None:
            return None
        p = _xpath_parser.new()
        try:
            return p.parse(expression)
        except SyntaxError, error:
            raise XsltException(Error.INVALID_EXPRESSION, expression, self.baseUri, self.lineNumber, self.columnNumber, str(error))

        return

    def parsePattern(self, pattern):
        """DEPRECATED: specify an attribute in 'legalAttrs' instead."""
        if pattern is None:
            return None
        p = _xpattern_parser.new()
        try:
            return p.parse(pattern)
        except SyntaxError, error:
            raise XsltException(Error.INVALID_PATTERN, pattern, self.baseUri, self.lineNumber, self.columnNumber, str(error))

        return

    def splitQName(self, qname):
        """DEPRECATED: specify an attribute in 'legalAttrs' instead."""
        if not qname:
            return None
        index = qname.find(':')
        if index != -1:
            split = (
             qname[:index], qname[index + 1:])
        else:
            split = (
             None, qname)
        return split
        return

    def expandQName(self, qname, refNode=None):
        """DEPRECATED: specify an attribute in 'legalAttrs' instead."""
        if not qname:
            return None
        if refNode:
            namespaces = GetAllNs(refNode)
        else:
            namespaces = self.namespaces
        (prefix, local) = self.splitQName(qname)
        if prefix:
            try:
                expanded = (
                 namespaces[prefix], local)
            except KeyError:
                raise XsltRuntimeException(Error.UNDEFINED_PREFIX, self, prefix)

        else:
            expanded = (
             EMPTY_NAMESPACE, local)
        return expanded
        return

    def instantiate(self, context, processor):
        """
        Implements default behavior of instantiating each child in the order
        that they appear in the stylesheet.
        """
        context.processorNss = self.namespaces
        context.currentInstruction = self
        for child in self.children:
            child.instantiate(context, processor)

        return

    def processChildren(self, context, processor):
        """
        Iterates over the children, instantiating them in the order that they
        appear in the stylesheet.
        """
        context.processorNss = self.namespaces
        context.currentInstruction = self
        for child in self.children:
            child.instantiate(context, processor)

        return

    def __str__(self):
        return '<XsltElement at 0x%x: name %r, %d attributes, %d children, precedence %d>' % (id(self), self.nodeName, len(self.attributes), len(self.children), self.importIndex)


class XsltText(XsltNode):
    __module__ = __name__
    nodeName = '#text'

    def __init__(self, root, baseUri, data):
        self.root = root
        self.baseUri = baseUri
        self.data = data
        return

    def instantiate(self, context, processor):
        processor.writers[(-1)].text(self.data)
        return

    def __str__(self):
        if len(self.data) > 20:
            data = self.data[:20] + '...'
        else:
            data = self.data
        return '<XsltText at 0x%x: %s>' % (id(self), repr(data))