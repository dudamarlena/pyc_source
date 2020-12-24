# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/bs4/builder/_lxml.py
# Compiled at: 2013-03-18 16:15:18
__all__ = ['LXMLTreeBuilderForXML',
 'LXMLTreeBuilder']
from StringIO import StringIO
import collections
from lxml import etree
from bs4.element import Comment, Doctype, NamespacedAttribute
from bs4.builder import FAST, HTML, HTMLTreeBuilder, PERMISSIVE, TreeBuilder, XML
from bs4.dammit import UnicodeDammit
LXML = 'lxml'

class LXMLTreeBuilderForXML(TreeBuilder):
    DEFAULT_PARSER_CLASS = etree.XMLParser
    is_xml = True
    features = [
     LXML, XML, FAST, PERMISSIVE]
    CHUNK_SIZE = 512

    @property
    def default_parser(self):
        return etree.XMLParser(target=self, strip_cdata=False, recover=True)

    def __init__(self, parser=None, empty_element_tags=None):
        if empty_element_tags is not None:
            self.empty_element_tags = set(empty_element_tags)
        if parser is None:
            parser = self.default_parser
        if isinstance(parser, collections.Callable):
            parser = parser(target=self, strip_cdata=False)
        self.parser = parser
        self.soup = None
        self.nsmaps = None
        return

    def _getNsTag(self, tag):
        if tag[0] == '{':
            return tuple(tag[1:].split('}', 1))
        else:
            return (
             None, tag)
            return

    def prepare_markup(self, markup, user_specified_encoding=None, document_declared_encoding=None):
        """
        :return: A 3-tuple (markup, original encoding, encoding
        declared within markup).
        """
        if isinstance(markup, unicode):
            return (markup, None, None, False)
        else:
            try_encodings = [
             user_specified_encoding, document_declared_encoding]
            dammit = UnicodeDammit(markup, try_encodings, is_html=True)
            return (dammit.markup, dammit.original_encoding,
             dammit.declared_html_encoding,
             dammit.contains_replacement_characters)

    def feed(self, markup):
        if isinstance(markup, basestring):
            markup = StringIO(markup)
        data = markup.read(self.CHUNK_SIZE)
        self.parser.feed(data)
        while data != '':
            data = markup.read(self.CHUNK_SIZE)
            if data != '':
                self.parser.feed(data)

        self.parser.close()

    def close(self):
        self.nsmaps = None
        return

    def start(self, name, attrs, nsmap={}):
        attrs = dict(attrs)
        nsprefix = None
        if len(nsmap) == 0 and self.nsmaps != None:
            self.nsmaps.append(None)
        elif len(nsmap) > 0:
            if self.nsmaps is None:
                self.nsmaps = []
            inverted_nsmap = dict((value, key) for key, value in nsmap.items())
            self.nsmaps.append(inverted_nsmap)
            attrs = attrs.copy()
            for prefix, namespace in nsmap.items():
                attribute = NamespacedAttribute('xmlns', prefix, 'http://www.w3.org/2000/xmlns/')
                attrs[attribute] = namespace

        if self.nsmaps is not None and len(self.nsmaps) > 0:
            new_attrs = {}
            for attr, value in attrs.items():
                namespace, attr = self._getNsTag(attr)
                if namespace is None:
                    new_attrs[attr] = value
                else:
                    nsprefix = self._prefix_for_namespace(namespace)
                    attr = NamespacedAttribute(nsprefix, attr, namespace)
                    new_attrs[attr] = value

            attrs = new_attrs
        namespace, name = self._getNsTag(name)
        nsprefix = self._prefix_for_namespace(namespace)
        self.soup.handle_starttag(name, namespace, nsprefix, attrs)
        return

    def _prefix_for_namespace(self, namespace):
        """Find the currently active prefix for the given namespace."""
        if namespace is None:
            return
        else:
            for inverted_nsmap in reversed(self.nsmaps):
                if inverted_nsmap is not None and namespace in inverted_nsmap:
                    return inverted_nsmap[namespace]

            return

    def end(self, name):
        self.soup.endData()
        completed_tag = self.soup.tagStack[(-1)]
        namespace, name = self._getNsTag(name)
        nsprefix = None
        if namespace is not None:
            for inverted_nsmap in reversed(self.nsmaps):
                if inverted_nsmap is not None and namespace in inverted_nsmap:
                    nsprefix = inverted_nsmap[namespace]
                    break

        self.soup.handle_endtag(name, nsprefix)
        if self.nsmaps != None:
            self.nsmaps.pop()
            if len(self.nsmaps) == 0:
                self.nsmaps = None
        return

    def pi(self, target, data):
        pass

    def data(self, content):
        self.soup.handle_data(content)

    def doctype(self, name, pubid, system):
        self.soup.endData()
        doctype = Doctype.for_name_and_ids(name, pubid, system)
        self.soup.object_was_parsed(doctype)

    def comment(self, content):
        """Handle comments as Comment objects."""
        self.soup.endData()
        self.soup.handle_data(content)
        self.soup.endData(Comment)

    def test_fragment_to_document(self, fragment):
        """See `TreeBuilder`."""
        return '<?xml version="1.0" encoding="utf-8"?>\n%s' % fragment


class LXMLTreeBuilder(HTMLTreeBuilder, LXMLTreeBuilderForXML):
    features = [
     LXML, HTML, FAST, PERMISSIVE]
    is_xml = False

    @property
    def default_parser(self):
        return etree.HTMLParser

    def feed(self, markup):
        self.parser.feed(markup)
        self.parser.close()

    def test_fragment_to_document(self, fragment):
        """See `TreeBuilder`."""
        return '<html><body>%s</body></html>' % fragment