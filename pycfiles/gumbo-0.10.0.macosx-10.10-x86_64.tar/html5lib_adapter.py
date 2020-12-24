# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/gumbo/html5lib_adapter.py
# Compiled at: 2015-04-30 22:50:43
"""Adapter between Gumbo and html5lib.

This exports one method, parse, with the same signature as html5lib.parse.  It
takes the text to parse, and optionally an html5lib TreeBuilder to build the
tree, and gives back a DOM tree in that format.  Example:

  doc = parse(text, treebuilder='lxml')
"""
__author__ = 'jdtang@google.com (Jonathan Tang)'
import gumboc
_NAMESPACES = [
 'http://www.w3.org/1999/xhtml',
 'http://www.w3.org/2000/svg',
 'http://www.w3.org/1998/Math/MathML']

def _convert_doctype(treebuilder, source_node):
    if not source_node.has_doctype:
        return
    treebuilder.insertDoctype({'name': source_node.name.decode('utf-8'), 
       'publicId': source_node.public_identifier.decode('utf-8'), 
       'systemId': source_node.system_identifier.decode('utf-8')})


def _convert_attributes(source_node):

    def maybe_namespace(attr):
        if attr.namespace != gumboc.AttributeNamespace.NONE:
            return (repr(attr.namespace).lower() if attr.name != 'xmlns' else None,
             attr.name.decode('utf-8'),
             attr.namespace.to_url())
        else:
            return attr.name.decode('utf-8')
            return

    return dict((maybe_namespace(attr), attr.value.decode('utf-8')) for attr in source_node.attributes)


def _convert_element(source_node):
    if source_node.type not in (gumboc.NodeType.ELEMENT, gumboc.NodeType.TEMPLATE):
        raise AssertionError('_convert_element only works with elements; found %r' % source_node.type)
    return {'name': source_node.v.element.tag_name.decode('utf-8'), 'namespace': _NAMESPACES[source_node.v.element.tag_namespace.value], 
       'data': _convert_attributes(source_node)}


def _insert_root(treebuilder, source_node, pop_element=True):
    treebuilder.insertRoot(_convert_element(source_node))
    for child_node in source_node.children:
        _insert_node(treebuilder, child_node)

    if pop_element:
        treebuilder.openElements.pop()


def _insert_node(treebuilder, source_node):
    assert source_node.type != gumboc.NodeType.DOCUMENT
    if source_node.type == gumboc.NodeType.COMMENT:
        treebuilder.insertComment({'data': source_node.v.text.text.decode('utf-8')})
    elif source_node.type in (
     gumboc.NodeType.TEXT,
     gumboc.NodeType.WHITESPACE,
     gumboc.NodeType.CDATA):
        treebuilder.insertText(source_node.v.text.text.decode('utf-8'))
    else:
        treebuilder.insertElementNormal(_convert_element(source_node))
        for child_node in source_node.v.element.children:
            _insert_node(treebuilder, child_node)

        treebuilder.openElements.pop()


class HTMLParser(object):

    def __init__(self, tree):
        self.tree = tree

    def parse(self, text_or_file, **kwargs):
        try:
            text = text_or_file.read()
        except AttributeError:
            text = text_or_file

        with gumboc.parse(text, **kwargs) as (output):
            _convert_doctype(self.tree, output.contents.document.contents)
            for node in output.contents.document.contents.children:
                if node.type == gumboc.NodeType.COMMENT:
                    self.tree.insertComment({'data': node.v.text.text.decode('utf-8')}, self.tree.document)
                elif node.type in (gumboc.NodeType.ELEMENT, gumboc.NodeType.TEMPLATE):
                    _insert_root(self.tree, output.contents.root.contents)
                elif not 'Only comments and <html> nodes allowed at the root':
                    raise AssertionError

            return self.tree.getDocument()

    def parseFragment(self, text_or_file, container, **kwargs):
        try:
            text = text_or_file.read()
        except AttributeError:
            text = text_or_file

        if ' ' in container:
            container_ns, container = container.split(' ')
        else:
            container_ns = 'html'
        with gumboc.parse(text, fragment_context=gumboc.Tag.from_str(container), fragment_namespace=getattr(gumboc.Namespace, container_ns.upper()), **kwargs) as (output):
            for node in output.contents.document.contents.children:
                if node.type in (gumboc.NodeType.ELEMENT, gumboc.NodeType.TEMPLATE):
                    _insert_root(self.tree, output.contents.root.contents, False)
                elif not 'Malformed fragment parse (??)':
                    raise AssertionError

            return self.tree.getFragment()