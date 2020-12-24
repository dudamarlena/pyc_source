# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\XUpdate.py
# Compiled at: 2005-08-02 17:42:59
__doc__ = '\nXUpdate request processing\n\nXUpdate is specified (poorly) at\nhttp://xmldb-org.sourceforge.net/xupdate/xupdate-wd.html\n\nCopyright 2005 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
__all__ = [
 'XUPDATE_NS', 'XUpdateException', 'g_errorMessages', 'StringWriter', 'SUPPORTED_VERSIONS', 'Processor', 'Reader', 'ApplyXUpdate']
XUPDATE_NS = 'http://www.xmldb.org/xupdate'
import string
from xml.dom import Node
from Ft import FtException
from Ft import TranslateMessage as _
from Ft.Xml import EMPTY_NAMESPACE, XML_NAMESPACE, Domlette
from Ft.Xml.Lib.XmlString import SplitQName, XmlStrStrip, IsXmlSpace
from Ft.Xml.XPath import g_parser as parser
from Ft.Xml.XPath import XPathTypes as Types
from Ft.Xml.XPath import Context, Conversions
from Ft.Xml.Xslt import NullWriter, DomWriter, AttributeValueTemplate
from Ft.Xml.Xslt.CopyOfElement import CopyNode

class XUpdateException(FtException):
    """
    Exception class for errors specific to XUpdate processing
    """
    __module__ = __name__
    SYNTAX_ERROR = 1
    UNRECOGNIZED_INSTRUCTION = 2
    NO_VERSION = 10
    NO_SELECT = 11
    NO_TEST = 12
    INVALID_SELECT = 13
    UNSUPPORTED_VERSION = 14
    INVALID_DOM_NODE = 100
    UNKNOWN_NODE_TYPE = 101

    def __init__(self, errorCode, *args, **kwargs):
        FtException.__init__(self, errorCode, g_errorMessages, args, **kwargs)


g_errorMessages = {XUpdateException.SYNTAX_ERROR: _('Syntax error in expression %(expr)r: %(err)s'), XUpdateException.UNRECOGNIZED_INSTRUCTION: _('Unrecognized instruction in XUpdate namespace: %(name)r'), XUpdateException.NO_VERSION: _('Missing required version attribute'), XUpdateException.NO_SELECT: _('Missing required select attribute'), XUpdateException.NO_TEST: _('Missing required "test" attribute'), XUpdateException.INVALID_SELECT: _('select expression "%(expr)s" must evaluate to a non-empty node-set'), XUpdateException.UNSUPPORTED_VERSION: _('XUpdate version %(version)s unsupported by this implementation'), XUpdateException.INVALID_DOM_NODE: _('Invalid DOM node %(node)r'), XUpdateException.UNKNOWN_NODE_TYPE: _('Unknown node type %(nodetype)r')}
SUPPORTED_VERSIONS = (
 '1.0',)

class StringWriter(NullWriter.NullWriter):
    __module__ = __name__

    def __init__(self):
        self._result = []

    def getResult(self):
        return ('').join(self._result)

    def text(self, data):
        self._result.append(data)
        return


class Processor:
    __module__ = __name__

    def __init__(self, reader=None):
        self.writers = [NullWriter.NullWriter(None)]
        return
        return

    def output(self):
        """Returns the current output writer"""
        return self.writers[(-1)]

    def pushDomResult(self, ownerDocument):
        self.writers.append(DomWriter.DomWriter(ownerDocument))
        return

    def pushStringResult(self):
        self.writers.append(StringWriter())
        return

    def popResult(self):
        return self.writers.pop().getResult()

    def execute(self, node, xupdate, variables=None, processorNss=None):
        if variables is None:
            variables = {}
        if processorNss is None:
            processorNss = {}
        context = Context.Context(node, varBindings=variables, processorNss=processorNss)
        self.visit(context, xupdate, 0)
        return node
        return

    def visit(self, context, node, preserveSpace):
        try:
            node_type = node.nodeType
        except AttributeError:
            raise XUpdateException(XUpdateException.INVALID_DOM_NODE, node=node)

        try:
            visit = self._dispatch_node[node_type]
        except KeyError:
            node_types = {}
            for name in dir(Node):
                if name.endswith('_NODE'):
                    node_types[getattr(Node, name)] = name

            node_type = node_types.get(node_type, node_type)
            raise XUpdateException(XUpdateException.INVALID_DOM_NODE, nodetype=node_type)
        else:
            visit(self, context, node, preserveSpace)

        return

    _dispatch_node = {}

    def _visit_document(self, context, node, preserveSpace):
        element = node.documentElement
        if element is not None and element.namespaceURI == XUPDATE_NS and element.localName == 'modifications':
            version = element.getAttributeNS(EMPTY_NAMESPACE, 'version')
            if not version:
                raise XUpdateException(XUpdateException.NO_VERSION)
            if version not in SUPPORTED_VERSIONS:
                raise XUpdateException(XUpdateException.UNSUPPORTED_VERSION, version=version)
            for node in element.childNodes:
                self.visit(context, node, preserveSpace)

        return
        return

    _dispatch_node[Node.DOCUMENT_NODE] = _visit_document

    def _visit_text(self, context, node, preserveSpace):
        if preserveSpace or not IsXmlSpace(node.data):
            self.writers[(-1)].text(node.data)
        return

    _dispatch_node[Node.TEXT_NODE] = _visit_text

    def _visit_element(self, context, element, preserveSpace):
        xml_space = element.getAttributeNS(XML_NAMESPACE, 'space')
        if xml_space == 'preserve':
            preserveSpace = 1
        elif xml_space == 'default':
            preserveSpace = 0
        if element.namespaceURI != XUPDATE_NS:
            self.writers[(-1)].startElement(element.nodeName, element.namespaceURI)
            for attr in element.attributes.values():
                self.writers[(-1)].attribute(attr.nodeName, attr.value, attr.namespaceURI)

            for node in element.childNodes:
                self.visit(context, node, preserveSpace)

            self.writers[(-1)].endElement(element.nodeName, element.namespaceURI)
        try:
            visit = self._dispatch_xupdate[element.localName]
        except KeyError:
            raise XUpdateException(XUpdateException.UNRECOGNIZED_INSTRUCTION, name=element.localName)
        else:
            visit(self, context, element, preserveSpace)

        return

    _dispatch_node[Node.ELEMENT_NODE] = _visit_element

    def _visit_ignorable(self, context, node, preserveSpace):
        return

    _dispatch_node[Node.COMMENT_NODE] = _visit_ignorable
    _dispatch_node[Node.PROCESSING_INSTRUCTION_NODE] = _visit_ignorable
    _dispatch_xupdate = {}

    def _xu_remove(self, context, element, preserveSpace):
        select = element.getAttributeNS(EMPTY_NAMESPACE, 'select')
        if not select:
            raise XUpdateException(XUpdateException.NO_SELECT)
        oldNss = context.processorNss
        context.processorNss = Domlette.GetAllNs(element)
        nodeset = self.evaluateExpression(context, select)
        if nodeset:
            refnode = nodeset[0]
            if refnode.nodeType == Node.ATTRIBUTE_NODE:
                parent = refnode.ownerElement
                parent.removeAttributeNode(refnode)
            else:
                parent = refnode.parentNode
                if parent is None:
                    parent = refnode.ownerDocument
                parent.removeChild(nodeset[0])
        context.processorNss = oldNss
        return
        return

    _dispatch_xupdate['remove'] = _xu_remove

    def _xu_append(self, context, element, preserveSpace):
        select = element.getAttributeNS(EMPTY_NAMESPACE, 'select')
        if not select:
            raise XUpdateException(XUpdateException.NO_SELECT)
        child = element.getAttributeNS(EMPTY_NAMESPACE, 'child') or 'last()'
        oldNss = context.processorNss
        context.processorNss = Domlette.GetAllNs(element)
        nodeset = self.evaluateExpression(context, select)
        if not isinstance(nodeset, Types.NodesetType) or not nodeset:
            raise XUpdateException(XUpdateException.INVALID_SELECT, expr=select)
        for refnode in nodeset:
            self.pushDomResult(refnode.ownerDocument)
            wrapper_localName = 'wrapper'
            wrapper_namespace = EMPTY_NAMESPACE
            try:
                self.writers[(-1)].startElement(wrapper_localName, wrapper_namespace)
                for node in element.childNodes:
                    self.visit(context, node, preserveSpace)

            finally:
                self.writers[(-1)].endElement(wrapper_localName, wrapper_namespace)
                result = self.popResult()
            size = len(refnode.childNodes)
            con = Context.Context(refnode, 1, size, processorNss={'xupdate': XUPDATE_NS})
            position = self.evaluateExpression(con, child)
            position = int(Conversions.NumberValue(position))
            wrapper = result.childNodes[0]
            if wrapper.attributes and hasattr(refnode, 'setAttributeNodeNS'):
                for attr in wrapper.attributes.values():
                    refnode.setAttributeNodeNS(attr)

            for node in tuple(wrapper.childNodes):
                if position >= size:
                    refnode.appendChild(node)
                else:
                    refnode.insertBefore(node, refnode.childNodes[position])

        context.processorNss = oldNss
        return

    _dispatch_xupdate['append'] = _xu_append

    def _xu_insert(self, context, element, preserveSpace):
        select = element.getAttributeNS(EMPTY_NAMESPACE, 'select')
        if not select:
            raise XUpdateException(XUpdateException.NO_SELECT)
        oldNss = context.processorNss
        context.processorNss = Domlette.GetAllNs(element)
        nodeset = self.evaluateExpression(context, select)
        if not nodeset:
            raise XUpdateException(XUpdateException.INVALID_SELECT, expr=select)
        for refnode in nodeset:
            self.pushDomResult(refnode.ownerDocument)
            try:
                for child in element.childNodes:
                    self.visit(context, child, preserveSpace)

            finally:
                result = self.popResult()
            if element.localName == 'insert-before':
                refnode.parentNode.insertBefore(result, refnode)
            elif element.localName == 'insert-after':
                refnode.parentNode.insertBefore(result, refnode.nextSibling)

        context.processorNss = oldNss
        return

    _dispatch_xupdate['insert-after'] = _xu_insert
    _dispatch_xupdate['insert-before'] = _xu_insert

    def _xu_update(self, context, element, preserveSpace):
        select = element.getAttributeNS(EMPTY_NAMESPACE, 'select')
        if not select:
            raise XUpdateException(XUpdateException.NO_SELECT)
        oldNss = context.processorNss
        context.processorNss = Domlette.GetAllNs(element)
        nodeset = self.evaluateExpression(context, select)
        if not nodeset:
            raise XUpdateException(XUpdateException.INVALID_SELECT, expr=select)
        refnode = nodeset[0]
        if refnode.nodeType == Node.ATTRIBUTE_NODE:
            self.pushStringResult()
            try:
                for child in element.childNodes:
                    self.visit(context, child, preserveSpace)

            finally:
                result = self.popResult()
            refnode.value = result
        else:
            self.pushDomResult(refnode.ownerDocument)
            try:
                for child in element.childNodes:
                    self.visit(context, child, preserveSpace)

            finally:
                result = self.popResult()
            while refnode.firstChild:
                refnode.removeChild(refnode.firstChild)

            refnode.appendChild(result)
        context.processorNss = oldNss
        return

    _dispatch_xupdate['update'] = _xu_update

    def _xu_rename(self, context, element, preserveSpace):
        select = element.getAttributeNS(EMPTY_NAMESPACE, 'select')
        if not select:
            raise XUpdateException(XUpdateException.NO_SELECT)
        oldNss = context.processorNss
        context.processorNss = Domlette.GetAllNs(element)
        nodeset = self.evaluateExpression(context, select)
        if not nodeset:
            raise XUpdateException(XUpdateException.INVALID_SELECT, expr=select)
        new_name = XmlStrStrip(element.firstChild.data)
        (prefix, local) = SplitQName(new_name)
        if prefix:
            namespace = context.processorNss[prefix]
        else:
            namespace = EMPTY_NAMESPACE
        for refnode in nodeset:
            if refnode.nodeType == Node.ATTRIBUTE_NODE:
                parent = refnode.ownerElement
                parent.removeAttributeNode(refnode)
                parent.setAttributeNS(namespace, new_name, refnode.value)
            else:
                parent = refnode.parentNode
                if parent is None:
                    parent = refnode.ownerDocument
                new_elem = refnode.ownerDocument.createElementNS(namespace, new_name)
                parent.replaceChild(new_elem, refnode)
                if refnode.attributes:
                    for attr in refnode.attributes.values():
                        new_elem.setAttributeNodeNS(attr)

                while refnode.firstChild:
                    new_elem.appendChild(refnode.firstChild)

        context.processorNss = oldNss
        return
        return

    _dispatch_xupdate['rename'] = _xu_rename

    def _xu_if(self, context, element, preserveSpace):
        test = element.getAttributeNS(EMPTY_NAMESPACE, 'test')
        if not test:
            raise XUpdateException(XUpdateException.NO_TEST)
        oldNss = context.processorNss
        context.processorNss = Domlette.GetAllNs(element)
        result = self.evaluateExpression(context, test)
        if Conversions.BooleanValue(result):
            for node in element.childNodes:
                self.visit(context, node, preserveSpace)

        context.processorNss = oldNss
        return

    _dispatch_xupdate['if'] = _xu_if

    def _xu_variable(self, context, element, preserveSpace):
        name = element.getAttributeNS(EMPTY_NAMESPACE, 'name')
        if not name:
            raise XUpdateException(XUpdateException.NO_NAME)
        select = element.getAttributeNS(EMPTY_NAMESPACE, 'select')
        if select:
            oldNss = context.processorNss
            context.processorNss = Domlette.GetAllNs(element)
            result = self.evaluateExpression(context, select)
            context.processorNss = oldNss
        else:
            result = Conversions.StringValue(element)
        (prefix, local) = SplitQName(name)
        if prefix:
            namespace = context.processorNss[prefix]
        else:
            namespace = EMPTY_NAMESPACE
        context.varBindings[(namespace, local)] = result
        return

    _dispatch_xupdate['variable'] = _xu_variable

    def _xu_element(self, context, element, preserveSpace):
        name = element.getAttributeNS(EMPTY_NAMESPACE, 'name')
        if not name:
            raise XUpdateException(XUpdateException.NO_NAME)
        _name = self.parseAVT(name)
        namespace = element.getAttributeNS(EMPTY_NAMESPACE, 'namespace')
        _namespace = self.parseAVT(namespace)
        oldNss = context.processorNss
        context.processorNss = Domlette.GetAllNs(element)
        name = _name.evaluate(context)
        namespace = _namespace and _namespace.evaluate(context)
        (prefix, local) = SplitQName(name)
        if not namespace:
            if prefix:
                namespace = context.processorNss[prefix]
            else:
                namespace = EMPTY_NAMESPACE
        self.writers[(-1)].startElement(name, namespace)
        for child in element.childNodes:
            self.visit(context, child, preserveSpace)

        self.writers[(-1)].endElement(name, namespace)
        context.processorNss = oldNss
        return

    _dispatch_xupdate['element'] = _xu_element

    def _xu_attribute(self, context, node, preserveSpace):
        name = node.getAttributeNS(EMPTY_NAMESPACE, 'name')
        if not name:
            raise XUpdateException(XUpdateException.NO_NAME)
        _name = self.parseAVT(name)
        namespace = node.getAttributeNS(EMPTY_NAMESPACE, 'namespace')
        _namespace = self.parseAVT(namespace)
        oldNss = context.processorNss
        context.processorNss = Domlette.GetAllNs(node)
        name = _name.evaluate(context)
        namespace = _namespace and _namespace.evaluate(context)
        (prefix, local) = SplitQName(name)
        if not namespace:
            if prefix:
                namespace = context.processorNss[prefix]
            else:
                namespace = EMPTY_NAMESPACE
        self.pushStringResult()
        try:
            for child in node.childNodes:
                self.visit(context, child, preserveSpace)

        finally:
            result = self.popResult()
        self.writers[(-1)].attribute(name, result, namespace)
        context.processorNss = oldNss
        return

    _dispatch_xupdate['attribute'] = _xu_attribute

    def _xu_text(self, context, element, preserveSpace):
        self.pushStringResult()
        try:
            for node in element.childNodes:
                self.visit(context, node, 1)

        finally:
            result = self.popResult()
        self.writers[(-1)].text(result)
        return

    _dispatch_xupdate['text'] = _xu_text

    def _xu_processing_instruction(self, context, element, preserveSpace):
        name = element.getAttributeNS(EMPTY_NAMESPACE, 'name')
        if not name:
            raise XUpdateException(XUpdateException.NO_NAME)
        _name = self.parseAVT(name)
        oldNss = context.processorNss
        context.processorNss = Domlette.GetAllNs(node)
        name = _name.evaluate(context)
        self.pushStringResult()
        try:
            for node in element.childNodes:
                self.visit(context, node, preserveSpace)

        finally:
            result = self.popResult()
        self.writers[(-1)].processingInstruction(name, result)
        context.processorNss = oldNss
        return

    _dispatch_xupdate['processing-instruction'] = _xu_processing_instruction

    def _xu_comment(self, context, element, preserveSpace):
        self.pushStringResult()
        try:
            for node in element.childNodes:
                self.visit(context, node, preserveSpace)

        finally:
            result = self.popResult()
        self.writers[(-1)].comment(result)
        return

    _dispatch_xupdate['comment'] = _xu_comment

    def _xu_value_of(self, context, element, preserveSpace):
        select = element.getAttributeNS(EMPTY_NAMESPACE, 'select')
        if not select:
            raise XUpdateException(XUpdateException.NO_SELECT)
        oldNss = context.processorNss
        context.processorNss = Domlette.GetAllNs(element)
        result = self.evaluateExpression(context, select)
        if isinstance(result, Types.NodesetType):
            for node in result:
                CopyNode(self, node)

        else:
            if not isinstance(result, Types.StringType):
                result = Conversions.StringValue(result)
            self.writers[(-1)].text(result)
        context.processorNss = oldNss
        return

    _dispatch_xupdate['value-of'] = _xu_value_of

    def evaluateExpression(self, context, expression):
        try:
            parsed_expr = parser.new().parse(expression)
        except SyntaxError, e:
            raise XUpdateException(XUpdateException.SYNTAX_ERROR, expr=expression, err=str(e))
        else:
            return parsed_expr.evaluate(context)

    def parseAVT(self, avt):
        if avt is None:
            return None
        return AttributeValueTemplate.AttributeValueTemplate(avt)
        return


class Reader(Domlette.NonvalidatingReaderBase):
    """
    A reader of XUpdate documents. Must contain a fromSrc() method
    that takes an Ft.Xml.InputSource and returns a Domlette document.
    It does not need to detect XUpdate syntax errors.
    """
    __module__ = __name__
    fromSrc = Domlette.NonvalidatingReaderBase.parse


def ApplyXUpdate(doc, xup):
    """
    Takes 2 InputSources, one for the source document and one for the
    XUpdate instructions.  It returns a DOM node representing the result
    of applying the XUpdate to the source document (the document is
    modified in-place).
    """
    reader = Domlette.NonvalidatingReader
    xureader = Reader()
    processor = Processor()
    source = reader.parse(doc)
    xupdate = xureader.fromSrc(xup)
    processor.execute(source, xupdate)
    return source


def ApplyXupdate(doc, xup):
    """
    Deprecated. Use ApplyXUpdate (only the name changed).
    """
    import warnings
    warnings.warn('Deprecated function ApplyXupdate called. Please use ApplyXUpdate (with a capital "U") instead.', DeprecationWarning, 2)
    return ApplyXUpdate(doc, xup)