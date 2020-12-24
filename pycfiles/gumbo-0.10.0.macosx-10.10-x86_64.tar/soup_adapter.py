# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/gumbo/soup_adapter.py
# Compiled at: 2015-04-30 22:50:43
"""Adapter between Gumbo and BeautifulSoup.

This parses an HTML document and gives back a BeautifulSoup object, which you
can then manipulate like a normal BeautifulSoup parse tree.
"""
__author__ = 'jdtang@google.com (Jonathan Tang)'
import BeautifulSoup, gumboc

def _utf8(text):
    return text.decode('utf-8', 'replace')


def _add_source_info(obj, original_text, start_pos, end_pos):
    obj.original = str(original_text)
    obj.line = start_pos.line
    obj.col = start_pos.column
    obj.offset = start_pos.offset
    if end_pos:
        obj.end_line = end_pos.line
        obj.end_col = end_pos.column
        obj.end_offset = end_pos.offset


def _convert_attrs(attrs):
    return [ (_utf8(attr.name), _utf8(attr.value)) for attr in attrs ]


def _add_document(soup, element):
    pass


def _add_element(soup, element):
    tag = BeautifulSoup.Tag(soup, _utf8(element.tag_name), _convert_attrs(element.attributes))
    for child in element.children:
        tag.append(_add_node(soup, child))

    _add_source_info(tag, element.original_tag, element.start_pos, element.end_pos)
    tag.original_end_tag = str(element.original_end_tag)
    return tag


def _add_text(cls):

    def add_text_internal(soup, element):
        text = cls(_utf8(element.text))
        _add_source_info(text, element.original_text, element.start_pos, None)
        return text

    return add_text_internal


_HANDLERS = [
 _add_document,
 _add_element,
 _add_text(BeautifulSoup.NavigableString),
 _add_text(BeautifulSoup.CData),
 _add_text(BeautifulSoup.Comment),
 _add_text(BeautifulSoup.NavigableString),
 _add_element]

def _add_node(soup, node):
    return _HANDLERS[node.type.value](soup, node.contents)


def _add_next_prev_pointers(soup):

    def _traverse(node):
        yield node
        try:
            for child in node.contents:
                for descendant in _traverse(child):
                    yield descendant

        except AttributeError:
            return

    nodes = sorted(_traverse(soup), key=lambda node: node.offset)
    if nodes:
        nodes[0].previous = None
        nodes[(-1)].next = None
    for i, node in enumerate(nodes[1:-1], 1):
        nodes[(i - 1)].next = node
        node.previous = nodes[(i - 1)]

    return


def parse(text, **kwargs):
    with gumboc.parse(text, **kwargs) as (output):
        soup = BeautifulSoup.BeautifulSoup()
        soup.append(_add_node(soup, output.contents.root.contents))
        _add_next_prev_pointers(soup)
        return soup