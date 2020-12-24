# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/rdfxml.py
# Compiled at: 2008-04-06 11:46:19
"""An in-memory store plugin for `rdf`.

This plugin is intended to be installed into rdf.plugins.parsers.

TODO: example usage.

"""
__version__ = '0.9a1'
from xml.sax import make_parser
from xml.sax.saxutils import handler, quoteattr, escape
from xml.sax.handler import ErrorHandler
from urlparse import urljoin, urldefrag
from rdf.parser import Parser
from rdf.term import URIRef, BNode, Literal
from rdf.term import RDF, RDFS
from rdf.term import is_ncname
from rdf.exceptions import ParserError, Error
UNQUALIFIED = {'about': RDF.about, 'ID': RDF.ID, 
   'type': RDF.type, 
   'resource': RDF.resource, 
   'parseType': RDF.parseType}
CORE_SYNTAX_TERMS = [
 RDF.RDF, RDF.ID, RDF.about, RDF.parseType, RDF.resource, RDF.nodeID, RDF.datatype]
SYNTAX_TERMS = CORE_SYNTAX_TERMS + [RDF.Description, RDF.li]
OLD_TERMS = [
 URIRef(RDF.uri + 'aboutEach'), URIRef(RDF.uri + 'aboutEachPrefix'), URIRef(RDF.uri + 'bagID')]
NODE_ELEMENT_EXCEPTIONS = CORE_SYNTAX_TERMS + [RDF.li] + OLD_TERMS
NODE_ELEMENT_ATTRIBUTES = [RDF.ID, RDF.nodeID, RDF.about]
PROPERTY_ELEMENT_EXCEPTIONS = CORE_SYNTAX_TERMS + [RDF.Description] + OLD_TERMS
PROPERTY_ATTRIBUTE_EXCEPTIONS = CORE_SYNTAX_TERMS + [RDF.Description, RDF.li] + OLD_TERMS
PROPERTY_ELEMENT_ATTRIBUTES = [RDF.ID, RDF.resource, RDF.nodeID]
XMLNS = 'http://www.w3.org/XML/1998/namespace'
BASE = (XMLNS, 'base')
LANG = (XMLNS, 'lang')

class BagID(URIRef):
    __slots__ = [
     'li']

    def __init__(self, val):
        super(URIRef, self).__init__(val)
        self.li = 0

    def next_li(self):
        self.li += 1
        return URIRef(RDF.uri + '_%s' % self.li)


class ElementHandler(object):
    __slots__ = [
     'start', 'char', 'end', 'li', 'id',
     'base', 'subject', 'predicate', 'object',
     'list', 'language', 'datatype', 'declared', 'data']

    def __init__(self):
        self.start = None
        self.char = None
        self.end = None
        self.li = 0
        self.id = None
        self.base = None
        self.subject = None
        self.object = None
        self.list = None
        self.language = None
        self.datatype = None
        self.declared = None
        self.data = None
        return

    def next_li(self):
        self.li += 1
        return URIRef(RDF.uri + '_%s' % self.li)


class RDFXMLHandler(handler.ContentHandler):

    def __init__(self, store):
        self.store = store
        self.preserve_bnode_ids = False
        self.reset()

    def reset(self):
        self.stack = []
        self.ids = {}
        self.bnode = {}
        self._ns_contexts = [{}]
        self._current_context = self._ns_contexts[(-1)]

    def setDocumentLocator(self, locator):
        self.locator = locator

    def startDocument(self):
        document = ElementHandler()
        document_element = ElementHandler()
        document_element.start = self.document_element_start
        document_element.end = lambda name, qname: None
        stack = self.stack
        stack.append(None)
        stack.append(document)
        stack.append(document_element)
        current = self.current
        systemId = self.locator.getPublicId() or self.locator.getSystemId()
        if systemId:
            current.base = systemId
        return

    def startPrefixMapping(self, prefix, namespace):
        self._ns_contexts.append(self._current_context.copy())
        self._current_context[namespace] = prefix
        namespace = self.absolutize(namespace)
        self.store.bind(prefix, namespace, override=False)

    def endPrefixMapping(self, prefix):
        self._current_context = self._ns_contexts[(-1)]
        del self._ns_contexts[-1]

    def startElementNS(self, name, qname, attrs):
        stack = self.stack
        stack.append(ElementHandler())
        current = self.current
        parent = self.parent
        base = attrs.get(BASE, None)
        if base is not None:
            (base, frag) = urldefrag(base)
            if parent and parent.base:
                base = urljoin(parent.base, base)
            else:
                systemId = self.locator.getPublicId() or self.locator.getSystemId()
                if systemId:
                    base = urljoin(systemId, base)
        else:
            if parent:
                base = parent.base
            if base is None:
                systemId = self.locator.getPublicId() or self.locator.getSystemId()
                if systemId:
                    (base, frag) = urldefrag(systemId)
        current.base = base
        language = attrs.get(LANG, None)
        if language is None:
            if parent:
                language = parent.language
        current.language = language
        current.start(name, qname, attrs)
        return

    def endElementNS(self, name, qname):
        self.current.end(name, qname)
        self.stack.pop()

    def characters(self, content):
        char = self.current.char
        if char:
            char(content)

    def ignorableWhitespace(self, content):
        pass

    def processingInstruction(self, target, data):
        pass

    def add_reified(self, sid, (s, p, o)):
        self.store.add((sid, RDF.type, RDF.Statement))
        self.store.add((sid, RDF.subject, s))
        self.store.add((sid, RDF.predicate, p))
        self.store.add((sid, RDF.object, o))

    def error(self, message):
        locator = self.locator
        info = '%s:%s:%s: ' % (locator.getSystemId(),
         locator.getLineNumber(), locator.getColumnNumber())
        raise ParserError(info + message)

    def get_current(self):
        return self.stack[(-2)]

    current = property(get_current)

    def get_next(self):
        return self.stack[(-1)]

    next = property(get_next)

    def get_parent(self):
        return self.stack[(-3)]

    parent = property(get_parent)

    def absolutize(self, uri):
        result = urljoin(self.current.base, uri, allow_fragments=1)
        if uri and uri[(-1)] == '#' and result[(-1)] != '#':
            result = '%s#' % result
        return URIRef(result)

    def convert(self, name, qname, attrs):
        if name[0] is None:
            name = URIRef(name[1])
        else:
            name = URIRef(('').join(name))
        atts = {}
        for (n, v) in attrs.items():
            if n[0] is None:
                att = URIRef(n[1])
            else:
                att = URIRef(('').join(n))
            if att.startswith(XMLNS) or att[0:3].lower() == 'xml':
                pass
            elif att in UNQUALIFIED:
                atts[URIRef(RDF.uri + att)] = v
            else:
                atts[URIRef(att)] = v

        return (
         name, atts)

    def document_element_start(self, name, qname, attrs):
        if name[0] and URIRef(('').join(name)) == RDF.RDF:
            next = self.next
            next.start = self.node_element_start
            next.end = self.node_element_end
        else:
            self.node_element_start(name, qname, attrs)

    def node_element_start(self, name, qname, attrs):
        (name, atts) = self.convert(name, qname, attrs)
        current = self.current
        absolutize = self.absolutize
        next = self.next
        next.start = self.property_element_start
        next.end = self.property_element_end
        if name in NODE_ELEMENT_EXCEPTIONS:
            self.error('Invalid node element URI: %s' % name)
        if RDF.ID in atts:
            if RDF.about in atts or RDF.nodeID in atts:
                self.error('Can have at most one of rdf:ID, rdf:about, and rdf:nodeID')
            id = atts[RDF.ID]
            if not is_ncname(id):
                self.error('rdf:ID value is not a valid NCName: %s' % id)
            subject = absolutize('#%s' % id)
            if subject in self.ids:
                self.error("two elements cannot use the same ID: '%s'" % subject)
            self.ids[subject] = 1
        elif RDF.nodeID in atts:
            if RDF.ID in atts or RDF.about in atts:
                self.error('Can have at most one of rdf:ID, rdf:about, and rdf:nodeID')
            nodeID = atts[RDF.nodeID]
            if not is_ncname(nodeID):
                self.error('rdf:nodeID value is not a valid NCName: %s' % nodeID)
            if self.preserve_bnode_ids is False:
                if nodeID in self.bnode:
                    subject = self.bnode[nodeID]
                else:
                    subject = BNode()
                    self.bnode[nodeID] = subject
            else:
                subject = BNode(nodeID)
        elif RDF.about in atts:
            if RDF.ID in atts or RDF.nodeID in atts:
                self.error('Can have at most one of rdf:ID, rdf:about, and rdf:nodeID')
            subject = absolutize(atts[RDF.about])
        else:
            subject = BNode()
        if name != RDF.Description:
            self.store.add((subject, RDF.type, absolutize(name)))
        language = current.language
        for att in atts:
            if not att.startswith(RDF.uri):
                predicate = absolutize(att)
                try:
                    object = Literal(atts[att], language)
                except Error, e:
                    self.error(e.msg)

            elif att == RDF.type:
                predicate = RDF.type
                object = absolutize(atts[RDF.type])
            elif att in NODE_ELEMENT_ATTRIBUTES:
                continue
            elif att in PROPERTY_ATTRIBUTE_EXCEPTIONS:
                self.error('Invalid property attribute URI: %s' % att)
                continue
            else:
                predicate = absolutize(att)
                try:
                    object = Literal(atts[att], language)
                except Error, e:
                    self.error(e.msg)

            self.store.add((subject, predicate, object))

        current.subject = subject

    def node_element_end(self, name, qname):
        self.parent.object = self.current.subject

    def property_element_start(self, name, qname, attrs):
        (name, atts) = self.convert(name, qname, attrs)
        current = self.current
        absolutize = self.absolutize
        next = self.next
        object = None
        current.data = None
        current.list = None
        if not name.startswith(RDF.uri):
            current.predicate = absolutize(name)
        elif name == RDF.li:
            current.predicate = current.next_li()
        elif name in PROPERTY_ELEMENT_EXCEPTIONS:
            self.error('Invalid property element URI: %s' % name)
        else:
            current.predicate = absolutize(name)
        id = atts.get(RDF.ID, None)
        if id is not None:
            if not is_ncname(id):
                self.error('rdf:ID value is not a value NCName: %s' % id)
            current.id = absolutize('#%s' % id)
        else:
            current.id = None
        resource = atts.get(RDF.resource, None)
        nodeID = atts.get(RDF.nodeID, None)
        parse_type = atts.get(RDF.parseType, None)
        if resource is not None and nodeID is not None:
            self.error('Property element cannot have both rdf:nodeID and rdf:resource')
        if resource is not None:
            object = absolutize(resource)
            next.start = self.node_element_start
            next.end = self.node_element_end
        elif nodeID is not None:
            if not is_ncname(nodeID):
                self.error('rdf:nodeID value is not a valid NCName: %s' % nodeID)
            if self.preserve_bnode_ids is False:
                if nodeID in self.bnode:
                    object = self.bnode[nodeID]
                else:
                    subject = BNode()
                    self.bnode[nodeID] = subject
                    object = subject
            else:
                object = subject = BNode(nodeID)
            next.start = self.node_element_start
            next.end = self.node_element_end
        elif parse_type is not None:
            for att in atts:
                if att != RDF.parseType and att != RDF.ID:
                    self.error("Property attr '%s' now allowed here" % att)

            if parse_type == 'Resource':
                current.subject = object = BNode()
                current.char = self.property_element_char
                next.start = self.property_element_start
                next.end = self.property_element_end
            elif parse_type == 'Collection':
                current.char = None
                object = current.list = RDF.nil
                next.start = self.node_element_start
                next.end = self.list_node_element_end
            else:
                object = Literal('', None, RDF.XMLLiteral)
                current.char = self.literal_element_char
                current.declared = {}
                next.start = self.literal_element_start
                next.char = self.literal_element_char
                next.end = self.literal_element_end
            current.object = object
            return
        else:
            object = None
            current.char = self.property_element_char
            next.start = self.node_element_start
            next.end = self.node_element_end
        datatype = current.datatype = atts.get(RDF.datatype, None)
        language = current.language
        if datatype is not None:
            current.datatype = absolutize(datatype)
        else:
            for att in atts:
                if not att.startswith(RDF.uri):
                    predicate = absolutize(att)
                elif att in PROPERTY_ELEMENT_ATTRIBUTES:
                    continue
                elif att in PROPERTY_ATTRIBUTE_EXCEPTIONS:
                    self.error('Invalid property attribute URI: %s' % att)
                else:
                    predicate = absolutize(att)
                if att == RDF.type:
                    o = URIRef(atts[att])
                else:
                    o = Literal(atts[att], language)
                if object is None:
                    object = BNode()
                self.store.add((object, predicate, o))

            if object is None:
                current.data = ''
                current.object = None
            current.data = None
            current.object = object
        return

    def property_element_char(self, data):
        current = self.current
        if current.data is not None:
            current.data += data
        return

    def property_element_end(self, name, qname):
        current = self.current
        if current.data is not None and current.object is None:
            if current.datatype is not None:
                current.object = Literal(current.data, datatype=current.datatype)
            else:
                current.object = Literal(current.data, current.language)
            current.data = None
        if self.next.end == self.list_node_element_end:
            if current.object != RDF.nil:
                self.store.add((current.list, RDF.rest, RDF.nil))
        if current.object is not None:
            self.store.add((self.parent.subject, current.predicate, current.object))
            if current.id is not None:
                self.add_reified(current.id, (self.parent.subject,
                 current.predicate, current.object))
        current.subject = None
        return

    def list_node_element_end(self, name, qname):
        current = self.current
        if self.parent.list == RDF.nil:
            list = BNode()
            self.parent.list = list
            self.store.add((self.parent.list, RDF.first, current.subject))
            self.parent.object = list
            self.parent.char = None
        else:
            list = BNode()
            self.store.add((self.parent.list, RDF.rest, list))
            self.store.add((list, RDF.first, current.subject))
            self.parent.list = list
        return

    def literal_element_start(self, name, qname, attrs):
        current = self.current
        self.next.start = self.literal_element_start
        self.next.char = self.literal_element_char
        self.next.end = self.literal_element_end
        current.declared = self.parent.declared.copy()
        if name[0]:
            prefix = self._current_context[name[0]]
            if prefix:
                current.object = '<%s:%s' % (prefix, name[1])
            else:
                current.object = '<%s' % name[1]
            if name[0] not in current.declared:
                current.declared[name[0]] = prefix
                if prefix:
                    current.object += ' xmlns:%s="%s"' % (prefix, name[0])
                else:
                    current.object += ' xmlns="%s"' % name[0]
        else:
            current.object = '<%s' % name[1]
        for (name, value) in attrs.items():
            if name[0]:
                if name[0] not in current.declared:
                    current.declared[name[0]] = self._current_context[name[0]]
                name = current.declared[name[0]] + ':' + name[1]
            else:
                name = name[1]
            current.object += ' %s=%s' % (name, quoteattr(value))

        current.object += '>'

    def literal_element_char(self, data):
        self.current.object += escape(data)

    def literal_element_end(self, name, qname):
        if name[0]:
            prefix = self._current_context[name[0]]
            if prefix:
                end = '</%s:%s>' % (prefix, name[1])
            else:
                end = '</%s>' % name[1]
        else:
            end = '</%s>' % name[1]
        self.parent.object += self.current.object + end


def create_parser(target, store):
    parser = make_parser()
    parser.start_namespace_decl('xml', 'http://www.w3.org/XML/1998/namespace')
    parser.setFeature(handler.feature_namespaces, 1)
    rdfxml = RDFXMLHandler(store)
    rdfxml.setDocumentLocator(target)
    parser.setContentHandler(rdfxml)
    parser.setErrorHandler(ErrorHandler())
    return parser


class RDFXML(Parser):

    def __init__(self):
        pass

    def parse(self, source, sink, **args):
        self._parser = create_parser(source, sink)
        content_handler = self._parser.getContentHandler()
        preserve_bnode_ids = args.get('preserve_bnode_ids', None)
        if preserve_bnode_ids is not None:
            content_handler.preserve_bnode_ids = preserve_bnode_ids
        self._parser.parse(source)
        return