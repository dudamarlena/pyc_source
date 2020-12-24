# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twiddler/elementtreeplus.py
# Compiled at: 2008-07-24 14:48:01
import string
from elementtree.ElementTree import _ElementInterface, XMLTreeBuilder
from elementtree.ElementTree import ElementTree as OriginalElementTree
from elementtree.ElementTree import TreeBuilder as OriginalTreeBuilder
from elementtree.ElementTree import XMLTreeBuilder as OriginalXMLTreeBuilder
from elementtree.ElementTree import _escape_attrib
from elementtree.ElementTree import _escape_cdata
from elementtree.ElementTree import _raise_serialization_error
from elementtree.ElementTree import Comment
from elementtree.ElementTree import fixtag
from interfaces import ITree, INode
from zope.interface import implements
from re import compile
whitespace_re = compile('\\s*')

class ElementPlus(_ElementInterface):
    implements(INode)
    parent = None
    _tree = None

    def index(self, element):
        return self._children.index(element)

    def insert(self, i, element):
        _tree = self._tree
        if _tree:
            indexes = _tree._indexes
            for elem in element.getiterator():
                elem._tree = _tree
                for index_name in indexes.keys():
                    value = elem.get(index_name)
                    if value:
                        index = indexes[index_name]
                        seq = index.get(value, [])
                        seq.append(elem)
                        index[value] = seq

        element.parent = self
        self._children.insert(i, element)

    def append(self, element):
        _tree = self._tree
        if _tree:
            indexes = _tree._indexes
            for elem in element.getiterator():
                elem._tree = _tree
                for index_name in indexes.keys():
                    value = elem.get(index_name)
                    if value:
                        index = indexes[index_name]
                        seq = index.get(value, [])
                        seq.append(elem)
                        index[value] = seq

        element.parent = self
        self._children.append(element)

    def remove(self, element):
        self._children.remove(element)
        _tree = self._tree
        if _tree:
            indexes = _tree._indexes
            for elem in element.getiterator():
                for index_name in indexes.keys():
                    value = elem.get(index_name)
                    if value:
                        index = indexes[index_name]
                        index[value].remove(elem)
                        if not index[value]:
                            del index[value]

                elem._tree = None

        element.parent = None
        return

    def set(self, key, value):
        if self._tree and key in self._tree._indexes.keys():
            index = self._tree._indexes[key]
            old_value = self.attrib.get(key)
            if old_value:
                index[old_value].remove(self)
                if not index[old_value]:
                    del index[old_value]
            seq = index.get(value, [])
            seq.append(self)
            index[value] = seq
        self.attrib[key] = value

    def delete(self, key):
        if key not in self.attrib:
            return
        if self._tree and key in self._tree._indexes.keys():
            value = self.attrib[key]
            index = self._tree._indexes[key]
            index[value].remove(self)
            if not index[value]:
                del index[value]
        del self.attrib[key]

    def findByAttribute(self, attribute, value):
        possible = self._tree._indexes[attribute][value]
        i = len(possible)
        while i:
            i -= 1
            curr = elem = possible[i]
            while curr.parent:
                if curr.parent is self:
                    return elem
                curr = curr.parent

        raise KeyError, value

    def search(self, value):
        for index in self._tree.indexes:
            try:
                e = self.findByAttribute(index, value)
            except KeyError:
                continue

            return e

        raise


class ElementTreePlus(OriginalElementTree):
    implements(ITree)

    def __init__(self, indexes=()):
        """
        Instantiate an ElementTreePlus.

        indexes is a tuple of strings containing the names of attributes
        to be indexed.
        """
        self._root = None
        self._indexes = {}
        for index in indexes:
            self._indexes[index] = {}

        self.indexes = indexes
        return

    def findByAttribute(self, attribute, value):
        return self._indexes[attribute][value][(-1)]

    def search(self, value):
        for index in self.indexes:
            try:
                e = self.findByAttribute(index, value)
            except KeyError:
                continue

            return e

        raise


def XMLDeclaration(decl, attributes, encoding):
    element = ElementPlus(XMLDeclaration, attributes)
    element.text = decl
    element.encoding = str(encoding)
    return element


def DocType(doctype, attributes):
    element = ElementPlus(DocType, attributes)
    element.text = doctype
    return element


class TreeBuilder(OriginalTreeBuilder):

    def __init__(self, indexes=()):
        OriginalTreeBuilder.__init__(self, ElementPlus)
        self._tree = ElementTreePlus(indexes)
        self.start(False, {})

    def start(self, tag, attrs):
        self._flush()
        self._last = elem = self._factory(tag, attrs)
        elem._tree = self._tree
        if self._elem:
            parent = self._elem[(-1)]
            parent.append(elem)
            elem.parent = parent
        self._elem.append(elem)
        self._tail = 0
        return elem

    def close(self):
        self.end(False)
        assert len(self._elem) == 0, 'missing end tags'
        assert self._last != None, 'missing toplevel element'
        self._tree._root = self._last
        return self._tree

    def _flush(self):
        if self._data:
            if self._last is not None:
                text = string.join(self._data, '')
                if self._tail:
                    assert self._last.tail is None, 'internal error (tail)'
                    m = whitespace_re.match(text)
                    self._last.tail = m.group(0)
                    text = text[m.end():]
                    if text:
                        e = ElementPlus(False, {})
                        e.text = text
                        self._last.parent.append(e)
                        self._last = e
                else:
                    assert self._last.text is None, 'internal error (text)'
                    self._last.text = text
            self._data = []
        return

    def comment(self, data):
        self._flush()
        elem = Comment(data)
        self._elem[(-1)].append(elem)
        self._last = elem
        self._tail = 1
        return elem

    def _index(self, index_name, index_value, elem):
        index = self._tree._indexes.get(index_name)
        if index is not None:
            seq = index.get(index_value, [])
            seq.append(elem)
            index[index_value] = seq
        return

    def XmlDecl(self, version, encoding, standalone):
        assert standalone == -1, "Don't know what to do with standalone"
        self._flush()
        index_name = 'id'
        index_value = '_etp_xmldecl'
        elem = XMLDeclaration("<?xml version='%s' encoding='%s'?>" % (
         version,
         encoding), {index_name: index_value}, encoding)
        self._elem[(-1)].append(elem)
        self._index(index_name, index_value, elem)
        elem.parent = self._elem[(-1)]
        self._last = elem
        self._tail = 1

    def StartDoctypeDecl(self, doctypeName, systemId, publicId, has_internal_subset):
        assert not has_internal_subset, "Don't know what to do with has_internal_subset"
        self._flush()
        index_name = 'id'
        index_value = '_etp_doctype'
        elem = DocType("<!DOCTYPE %s PUBLIC '%s' '%s'>" % (
         doctypeName,
         publicId,
         systemId), {index_name: index_value})
        self._elem[(-1)].append(elem)
        self._index(index_name, index_value, elem)
        elem.parent = self._elem[(-1)]
        self._last = elem
        self._tail = 1


class XMLTreeBuilder(OriginalXMLTreeBuilder):
    isCData = False

    def __init__(self, indexes=()):
        from xml.parsers import expat
        self._parser = parser = expat.ParserCreate()
        target = TreeBuilder(indexes)
        self._target = target
        self._names = {}
        parser.DefaultHandlerExpand = self._default
        parser.StartElementHandler = self._start
        parser.EndElementHandler = self._end
        parser.CharacterDataHandler = self._data
        parser.StartCdataSectionHandler = self._cdata_start
        parser.EndCdataSectionHandler = self._cdata_end
        parser.CommentHandler = target.comment
        parser.XmlDeclHandler = target.XmlDecl
        parser.StartDoctypeDeclHandler = target.StartDoctypeDecl
        parser.UseForeignDTD()
        try:
            self._parser.buffer_text = 1
        except AttributeError:
            pass

        try:
            self._parser.ordered_attributes = 1
            self._parser.specified_attributes = 1
            parser.StartElementHandler = self._start_list
        except AttributeError:
            pass

        self._doctype = None
        self.entity = {}
        return

    def _cdata_start(self):
        self.isCData = True
        self._target.data('<![CDATA[')

    def _cdata_end(self):
        self.isCData = False
        self._target.data(']]>')

    def _fixtext(self, text):
        if not self.isCData:
            text = _escape_cdata(text)
        return text

    def _default(self, text):
        prefix = text[:1]
        if prefix == '&':
            try:
                self._target.data(self.entity[text[1:-1]])
            except KeyError:
                self._target.data(text)

        elif prefix == '<' and text[:9] == '<!DOCTYPE':
            self._doctype = []
        elif self._doctype is not None:
            if prefix == '>':
                self._doctype = None
                return
            text = string.strip(text)
            if not text:
                return
            self._doctype.append(text)
            n = len(self._doctype)
            if n > 2:
                type = self._doctype[1]
                if type == 'PUBLIC' and n == 4:
                    (name, type, pubid, system) = self._doctype
                elif type == 'SYSTEM' and n == 3:
                    (name, type, system) = self._doctype
                    pubid = None
                else:
                    return
                if pubid:
                    pubid = pubid[1:-1]
                self.doctype(name, pubid, system[1:-1])
                self._doctype = None
        else:
            self._data(text)
        return


def XML(text, indexes=()):
    parser = XMLTreeBuilder(indexes)
    if not text.strip():
        e = ElementPlus(False, {})
        e.text = unicode(text)
        tree = ElementTreePlus(indexes)
        tree._root = e
        e._tree = e
        return tree
    parser.feed(text)
    return parser.close()