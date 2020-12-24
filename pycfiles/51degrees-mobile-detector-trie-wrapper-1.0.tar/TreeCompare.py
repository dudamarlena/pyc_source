# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\Lib\TreeCompare.py
# Compiled at: 2005-03-18 19:47:16
__doc__ = '\nComparison functions for XML and HTML documents\n(mainly used in the test suites)\n\nCopyright 2005 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
import re, sgmllib
from sgmllib import SGMLParser
from xml.dom import Node
sgmllib.tagfind = re.compile('[a-zA-Z][-:_.a-zA-Z0-9]*')
sgmllib.attrfind = re.compile('\\s*([a-zA-Z_][-:_.a-zA-Z0-9]*)(\\s*=\\s*(\\\'[^\\\']*\\\'|"[^"]*"|\\S*))?')
from Ft.Lib.Uri import BASIC_RESOLVER, OsPathToUri
from Ft.Xml import Domlette, InputSource, XMLNS_NAMESPACE
from Ft.Xml.Lib.XmlString import XmlStrStrip, IsXmlSpace
import HtmlPrinter
FORBIDDEN_END_ELEMENTS = HtmlPrinter.HtmlPrinter.forbiddenEndElements.keys()
del HtmlPrinter
_S = '[ \t\r\n]'
_OptionalS = _S + '?'
_VersionNum = '[a-zA-Z0-9_.:-]+'
_Eq = '%s?=%s?' % (_S, _S)
_VersionInfo = _S + 'version' + _Eq + "(?:(?:'" + _VersionNum + "')|" + '(?:"' + _VersionNum + '"))'
_EncName = '[A-Za-z][A-Za-z0-9._-]*'
_EncodingDecl = _S + 'encoding' + _Eq + "(?:(?:'" + _EncName + "')|" + '(?:"' + _EncName + '"))'
_SDDecl = _S + 'standalone' + _Eq + "(?:(?:'(?:yes|no)')|" + '(?:"(?:yes|no)"))'
g_xmlTest = re.compile('<\\?xml' + '(?P<VersionInfo>%s)' % _VersionInfo + '(?P<EncodingDecl>%s)?' % _EncodingDecl + '(?P<SDDecl>%s)?' % _SDDecl + '%s?\\?>' % _S)
g_doctypeTest = re.compile('(<!DOCTYPE[ \t\r\n])')
g_htmlTest = re.compile('(<!doctype html)|(<html)', re.IGNORECASE)

def HtmlTreeCompare(expected, compared):
    """
    Compare two HTML strings.  The result is similar to the builtin cmp()
    function such that non-zero indicates non equal and zero means equal.
    """
    return not CompareHTML(expected, compared)


def XmlTreeCompare(expected, compared):
    match = g_xmlTest.match(expected)
    if match and match.groupdict().get('SDDecl'):
        asEntity = False
    else:
        asEntity = not g_doctypeTest.search(expected)
    return TreeCompare(expected, compared, asEntity=asEntity)


def NoWsTreeCompare(expected, compared):
    """
    Equivalent to calling TreeCompare() with ignoreWhitespace=1.
    """
    return TreeCompare(expected, compared, ignoreWhitespace=1)


from Ft.Xml import READ_EXTERNAL_DTD

def TreeCompare(expected, compared, ignoreWhitespace=0, baseUri=None, readExtDtd=READ_EXTERNAL_DTD, ignoreNsDecls=0, asEntity=False):
    """
    A cmp()-like function that compares two XML or HTML strings and
    has the side effect of reporting differences to stdout. Returns
    false if the nodes compare equal.

    XML strings are parsed into a Domlette and compared node-by-node.
    HTML strings are parsed with an SGML parser and are compared
    event-by-event. The markup type is guessed based on clues in the
    expected string.

    ignoreWhitespace controls whether whitespace differences in text
    nodes are ignored.

    'file:' URIs based on the current working directory are generated
    for each document. The baseUri argument is an optional absolute URI
    to use as the basis of the generated URIs, if a 'file' URI is
    undesirable.

    readExtDtd controls whether the external DTD subset is read
    when parsing XML. It does not affect the reading of external
    entities declared in the internal DTD subset.

    ignoreNsDecls controls whether namespace declarations are ignored
    when comparing XML documents.
    """
    if not g_xmlTest.match(expected) and g_htmlTest.search(expected):
        return not CompareHTML(expected, compared, ignoreWhitespace)
    if not baseUri:
        uri = OsPathToUri('expected', attemptAbsolute=True)
    else:
        uri = BASIC_RESOLVER.normalize('expected', baseUri)
    try:
        if asEntity:
            reader = Domlette.EntityReader
        elif readExtDtd:
            reader = Domlette.NonvalidatingReader
        else:
            reader = Domlette.NoExtDtdReader
        doc1 = reader.parseString(str(expected), uri)
    except:
        print '--- Expected ---'
        print expected
        raise

    if not baseUri:
        uri = OsPathToUri('expected', attemptAbsolute=True)
    else:
        uri = BASIC_RESOLVER.normalize('compared', baseUri)
    try:
        doc2 = reader.parseString(compared, uri)
    except:
        print '--- Compared ---'
        print compared
        raise

    if asEntity:
        _TryEntityAsDocumentEntity(doc1)
        _TryEntityAsDocumentEntity(doc2)
    result = NodeCompare(doc1, doc2, ignoreWhitespace=ignoreWhitespace, ignoreNsDecls=ignoreNsDecls)
    return not result


def _TryEntityAsDocumentEntity(entity):
    elements = 0
    for node in entity.childNodes:
        elements += int(node.nodeType == Node.ELEMENT_NODE)

    if elements == 1:
        nodes = [ x for x in entity.childNodes if x.nodeType == Node.TEXT_NODE and IsXmlSpace(x.data) ]
        for node in nodes:
            entity.removeChild(node)

    return


def NodeCompare(node1, node2, ignoreWhitespace=0, ignoreComments=0, ignoreNsDecls=0):
    """
    A function that compares two XML DOM nodes by traversing their
    attributes and descendants recursively until a mismatch is found.
    It has the side effect of reporting differences to stdout. Returns
    true if the nodes compare equal.

    ignoreWhitespace controls whether whitespace differences in text
    nodes are ignored.

    ignoreComments controls whether comment nodes are ignored.

    ignoreNsDecls controls whether namespace declarations are ignored.
    """
    if node1.nodeType != node2.nodeType:
        return __ReportError(node1, node2, 'nodeType')
    if node1.nodeType in (Node.DOCUMENT_NODE, Node.DOCUMENT_FRAGMENT_NODE):
        if ignoreComments:
            children1 = filter(lambda n: n.nodeType != Node.COMMENT_NODE, node1.childNodes)
            children2 = filter(lambda n: n.nodeType != Node.COMMENT_NODE, node2.childNodes)
        else:
            children1 = node1.childNodes
            children2 = node2.childNodes
        for (child1, child2) in map(None, children1, children2):
            if not NodeCompare(child1, child2, ignoreWhitespace, ignoreComments, ignoreNsDecls):
                return 0

    elif node1.nodeType == Node.DOCUMENT_TYPE_NODE:
        if node1.name != node2.name:
            return __ReportError(node1, node2, 'name')
        if node1.publicId != node2.publicId:
            return __ReportError(node1, node2, 'publicId')
        if node1.systemId != node2.systemId:
            return __ReportError(node1, node2, 'systemId')
        if node1.internalSubset != node2.internalSubset:
            return __ReportError(node1, node2, 'internalSubset')
        if len(node1.entities) != len(node2.entities):
            return __ReportError(node1, node2, 'entities')
        if len(node1.notations) != len(node2.notations):
            return __ReportError(node1, node2, 'notations')
    elif node1.nodeType == Node.ELEMENT_NODE:
        if node1.localName != node2.localName:
            return __ReportError(node1, node2, 'localName')
        if node1.namespaceURI != node2.namespaceURI:
            return __ReportError(node1, node2, 'namespaceURI')
        attrs1 = node1.attributes.values()
        attrs2 = node2.attributes.values()
        if ignoreNsDecls:
            attrs1 = [ a for a in attrs1 if a.namespaceURI != XMLNS_NAMESPACE ]
            attrs2 = [ a for a in attrs2 if a.namespaceURI != XMLNS_NAMESPACE ]
        if len(attrs1) != len(attrs2):
            return __ReportError(node1, node2, 'attributes')
        attrs1.sort(lambda a, b: cmp(a.name, b.name))
        attrs2.sort(lambda a, b: cmp(a.name, b.name))
        for (attr1, attr2) in zip(attrs1, attrs2):
            if attr1.localName != attr2.localName:
                print node1.attributes.keys()
                print node2.attributes.keys()
                return __ReportError(attr1, attr2, 'localName')
            if attr1.namespaceURI != attr2.namespaceURI:
                return __ReportError(attr1, attr2, 'namespaceURI')

        if ignoreComments:
            children1 = [ c for c in node1.childNodes if c.nodeType != Node.COMMENT_NODE ]
            children2 = [ c for c in node2.childNodes if c.nodeType != Node.COMMENT_NODE ]
        else:
            children1 = node1.childNodes
            children2 = node2.childNodes
        if len(children1) != len(children2):
            return __ReportError(node1, node2, 'childNodes')
        for (child1, child2) in zip(children1, children2):
            if not NodeCompare(child1, child2, ignoreWhitespace, ignoreComments, ignoreNsDecls):
                return 0

    else:
        if node1.nodeType == Node.TEXT_NODE:
            text1 = node1.data
            text2 = node2.data
            if ignoreWhitespace:
                if IsXmlSpace(text1):
                    text1 = None
                if IsXmlSpace(text2):
                    text2 = None
            if cmp(text1, text2):
                return __ReportError(node1, node2, 'data')
        if node1.nodeType == Node.COMMENT_NODE:
            if node1.data != node2.data:
                return __ReportError(node1, node2, 'data')
        elif node1.nodeType == Node.PROCESSING_INSTRUCTION_NODE:
            if node1.target != node2.target:
                return __ReportError(node1, node2, 'target')
            if node1.data != node2.data:
                return __ReportError(node1, node2, 'data')
    return 1
    return


def __ReportError(node1, node2, attribute):
    import pprint
    print '--- expected ---'
    __PrintParentage(node1)
    print 'node: %s' % repr(node1)
    print 'node.%s:' % attribute
    pprint.pprint(getattr(node1, attribute))
    print '--- compared ---'
    __PrintParentage(node2)
    print 'node: %s' % repr(node2)
    print 'node.%s:' % attribute
    pprint.pprint(getattr(node2, attribute))
    return 0


def __PrintParentage(node):
    nodes = [
     node]
    if node.nodeType == Node.ATTRIBUTE_NODE:
        parent = node.ownerElement
    else:
        parent = node.parentNode
    while parent:
        nodes.insert(0, parent)
        parent = parent.parentNode

    indent = ''
    for node in nodes:
        print '%s%s' % (indent, node.nodeName)
        indent = indent + '  '


class SGMLParserEventGenerator(SGMLParser):
    """
    An HTML parser that meets our needs better than Python's
    htmllib.HTMLParser, and that works with Python 2.1.

    Used by CompareHTML().
    """
    __module__ = __name__
    TEXT_EVENT = 1
    COMMENT_EVENT = 2
    START_TAG_EVENT = 3
    END_TAG_EVENT = 4
    ENTITYREF_EVENT = 6
    CHARREF_EVENT = 7

    def __init__(self, verbose=0):
        self.testdata = ''
        SGMLParser.__init__(self, verbose)
        self.events = []
        self.ignoreable_ws = 1

    def handle_data(self, data):
        self.testdata = self.testdata + data

    def flush(self):
        data = self.testdata
        if data:
            self.testdata = ''
            if not self.ignoreable_ws:
                self.events.append((self.TEXT_EVENT, data))

    def handle_comment(self, data):
        self.flush()
        self.events.append((self.COMMENT_EVENT, data))

    def unknown_starttag(self, tagname, attrs):
        self.flush()
        if self.ignoreable_ws:
            self.ignoreable_ws = 0
        dict = {}
        for (name, value) in attrs:
            dict[name] = value

        self.events.append((self.START_TAG_EVENT, tagname, dict))
        if tagname.lower() in FORBIDDEN_END_ELEMENTS:
            self.events.append((self.END_TAG_EVENT, tagname))
        return

    def unknown_endtag(self, tag):
        self.flush()
        self.events.append((self.END_TAG_EVENT, tag))

    def unknown_entityref(self, ref):
        self.flush()
        self.events.append((self.ENTITYREF_EVENT, ref))

    def unknown_charref(self, ref):
        self.flush()
        self.events.append((self.CHARREF_EVENT, ref))

    def close(self):
        SGMLParser.close(self)
        self.flush()


g_xmlEmptyTagPattern = re.compile('<([a-zA-Z][-:_.a-zA-Z0-9]*\\s*([a-zA-Z_][-:_.a-zA-Z0-9]*)(\\s*=\\s*(\\\'[^\\\']*\\\'|"[^"]*"|\\S*))?)/>')

def CompareHTML(html1, html2, ignoreWhitespace=0):
    """
    A cmp()-like function that compares two HTML strings by parsing
    with sgmllib.SGMLParser and comparing events until a mismatch is
    found. It has the side effect of reporting differences to stdout.

    ignoreWhitespace controls whether whitespace differences in text
    events are ignored.
    """
    html1 = g_xmlEmptyTagPattern.sub('<\\1>', html1)
    html2 = g_xmlEmptyTagPattern.sub('<\\1>', html2)
    p1 = SGMLParserEventGenerator()
    p1.feed(html1)
    p1.close()
    p2 = SGMLParserEventGenerator()
    p2.feed(html2)
    p2.close()
    stack = []
    for (cur1, cur2) in zip(p1.events, p2.events):
        if cur1[0] != cur2[0]:
            return __ReportEventError(cur1, cur2, stack, 'different events')
        event = cur1[0]
        if event == SGMLParserEventGenerator.TEXT_EVENT:
            d1 = cur1[1]
            d2 = cur2[1]
            if ignoreWhitespace and XmlStrStrip(d1) != XmlStrStrip(d2):
                return __ReportEventError(cur1, cur2, stack, 'data')
        elif event == SGMLParserEventGenerator.COMMENT_EVENT:
            d1 = cur1[1]
            d2 = cur2[1]
            if d1.strip() != d2.strip():
                return __ReportEventError(cur1, cur2, stack, 'comment data')
        elif event == SGMLParserEventGenerator.START_TAG_EVENT:
            if cur1[1] != cur2[1]:
                return __ReportEventError(cur1, cur2, stack, 'start tag name')
            stack.append(cur1[1])
            att1 = cur1[2]
            att2 = cur2[2]
            if len(att1) != len(att2):
                return __ReportEventError(cur1, cur2, stack, 'number of attributes')
            for (name, value) in att1.items():
                if att2.get(name, -1) != value:
                    return __ReportEventError(cur1, cur2, stack, 'attribute value %s' % name)

        elif event == SGMLParserEventGenerator.END_TAG_EVENT:
            if cur1[1] != cur2[1]:
                return __ReportEventError(cur1, cur2, stack, 'end tag name')
            while stack and stack[(-1)] != cur1[1]:
                del stack[-1]

            del stack[-1]
        elif event == SGMLParserEventGenerator.ENTITYREF_EVENT:
            if cur1[1] != cur2[1]:
                return __ReportEventError(cur1, cur2, stack, 'entity ref')
        elif event == SGMLParserEventGenerator.CHARREF_EVENT:
            if cur1[1] != cur2[1]:
                return __ReportEventError(cur1, cur2, stack, 'char ref')
        else:
            raise cur1

    return 1


def __ReportEventError(event1, event2, stack, attribute):
    __PrintStack(stack)
    print '--- Expected ---'
    print attribute, repr(event1[1:])
    print '--- Compared ---'
    print attribute, repr(event2[1:])
    return 0


def __PrintStack(stack):
    indent = ''
    for name in stack:
        print '%s%s' % (indent, name)
        indent += '  '