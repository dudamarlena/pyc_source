# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/parser.py
# Compiled at: 2016-12-08 16:29:22
from __future__ import unicode_literals
from __future__ import print_function
from lxml import etree
import re
from collections import defaultdict
import io, logging
from . import errors
from . import tags
from .tools import datetime_to_epoch
from .document import Document, DocumentStructure, DocumentNode, DocumentTextNode
from . import namespaces
from .containers import OrderedDict
from .cache.dictcache import DictCache
from .compat import text_type, string_types, binary_type
from fs.path import abspath
from fs.errors import NoSysPath
_re_xml_namespace = re.compile(b'^(?:\\{(.*?)\\})*(.*)$', re.UNICODE)
element_fromstring = etree.fromstring
log = logging.getLogger(b'moya.startup')

def extract_namespace(tag_name, _cache={}):
    """Extracts namespace and tag name in Clark's notation"""
    try:
        return _cache[tag_name]
    except KeyError:
        _cache[tag_name] = ns = _re_xml_namespace.match(tag_name).groups()
        return ns


class Parser(object):
    _default_cache = DictCache(b'parser', b'')

    def __init__(self, archive, fs, path, library=None):
        self.built = False
        try:
            self.cache = archive.get_cache(b'parser')
        except Exception as e:
            self.cache = self._default_cache

        self.archive = archive
        self.fs = fs
        self.path = abspath(path)
        self.library = library
        try:
            syspath = self.fs.getsyspath(path)
        except NoSysPath:
            syspath = None

        if syspath is None:
            self.location = self.fs.desc(path)
        else:
            self.location = syspath
        self._xml = None
        return

    @property
    def xml(self):
        if self._xml is None:
            xml = self.fs.getbytes(self.path)
            xml = xml.replace(b'\t', b'    ')
            self._xml = xml
        return self._xml

    def parse(self, _extract_namespace=extract_namespace, _DocumentTextNode=DocumentTextNode, _DocumentNode=DocumentNode, _binary_type=binary_type):
        location = self.location
        document = Document(self.archive, lib=self.library, path=self.path)
        document.location = location
        default_namespace = namespaces.default
        xml = self.xml
        if xml.isspace() or not xml:
            log.warning((b"file '{}' is empty").format(self.location))
            return
        else:
            structure = document.structure = DocumentStructure(document, self.library, xml)
            parser = etree.XMLParser()
            try:
                root = etree.parse(io.BytesIO(self.xml), parser).getroot()
            except Exception as e:
                error = getattr(e, b'msg', None) or text_type(e)
                raise errors.ParseError((b'XML failed to parse ({})').format(error), path=location, position=getattr(e, b'position', (1,
                                                                                                                                      1)), code=xml)

            stack = [(root, None)]

            def make_unicode(s):
                if isinstance(s, _binary_type):
                    return s.decode(b'utf-8')
                return s

            add_namespace = self.archive.known_namespaces.add
            while stack:
                node, parent_doc_id = stack.pop()
                if not isinstance(node.tag, string_types):
                    continue
                xmlns, tag_name = _extract_namespace(make_unicode(node.tag))
                if xmlns is None:
                    xmlns = default_namespace
                add_namespace(xmlns)
                translate_text = False
                if tag_name.startswith(b'_'):
                    tag_name = tag_name[1:]
                    translate_text = True
                attrs = defaultdict(OrderedDict)
                translatable_attrs = set()
                for k, v in node.items():
                    attr_ns, attr_name = _extract_namespace(make_unicode(k))
                    if attr_name.startswith(b'_'):
                        attr_name = attr_name[1:]
                        translatable_attrs.add(attr_name)
                    attrs[(attr_ns or default_namespace)][attr_name] = make_unicode(v)

                source_line = getattr(node, b'sourceline', None)
                doc_node = _DocumentNode(xmlns, tag_name, parent_doc_id, attrs, translatable_attrs, make_unicode(node.text), source_line, translate_text=translate_text)
                structure.add_node(doc_node)
                if node.tail:
                    text_node = _DocumentTextNode(parent_doc_id, source_line, make_unicode(node.tail))
                    structure.add_node(text_node)
                if node.text:
                    doc_text_node = _DocumentTextNode(doc_node.doc_id, doc_node.source_line, make_unicode(node.text))
                    structure.add_node(doc_text_node)
                stack.extend((child, doc_node.doc_id) for child in reversed(node))

            self.built = False
            return document


if __name__ == b'__main__':
    test = b'<logic xmlns="http://moyaproject.com">\n\n\n<dict dst="fruit">\n    <int dst="apples">3</int>\n    <int dst="pears">7</int>\n    <int dst="strawberries">10</int>\n</dict>\n\n<int dst="count" value="5" />\n<while test="count">\n    <debug>Count is ${count}</debug>\n    <dec dst="count"/>\n</while>\n<eval dst="L">["apples", "oranges", "pears"]</eval>\n<for src="L" dst="word">\n    <for src="word" dst="c"><debug>${c}</debug></for>\n    <debug>${word}</debug>\n</for>\n\n<dict dst="foo"/>\n<str dst="foo.bar" value="Hello!"/>\n<dict dst="foo" ifnot="foo" />\n<debug>${foo.bar}</debug>\n<frame context="foo">\n    <str dst="bar" value="Bye!"/>\n    <debug>${bar}</debug>\n    <debug>${.foo.bar}</debug>\n</frame>\n<debug>${foo.bar}</debug>\n</logic>\n\n'
    test = b'<moya xmlns="http://moyaproject.com" xmlns:let="http://moyaproject.com/let">\n\n<content libname="hello">\n    <call let:foo="bar"/>\n    <header>Hello</header>\n    World\n</content>\n\n</moya>'
    document_structure = Parser.parse_structure(test)
    document_structure.render()