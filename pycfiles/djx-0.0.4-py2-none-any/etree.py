# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-HZd96S/pip/pip/_vendor/html5lib/treewalkers/etree.py
# Compiled at: 2019-02-14 00:35:07
from __future__ import absolute_import, division, unicode_literals
from collections import OrderedDict
import re
from pip._vendor.six import string_types
from . import base
from .._utils import moduleFactoryFactory
tag_regexp = re.compile(b'{([^}]*)}(.*)')

def getETreeBuilder(ElementTreeImplementation):
    ElementTree = ElementTreeImplementation
    ElementTreeCommentType = ElementTree.Comment(b'asd').tag

    class TreeWalker(base.NonRecursiveTreeWalker):
        """Given the particular ElementTree representation, this implementation,
        to avoid using recursion, returns "nodes" as tuples with the following
        content:

        1. The current element

        2. The index of the element relative to its parent

        3. A stack of ancestor elements

        4. A flag "text", "tail" or None to indicate if the current node is a
           text node; either the text or tail of the current element (1)
        """

        def getNodeDetails(self, node):
            if isinstance(node, tuple):
                elt, _, _, flag = node
                if flag in ('text', 'tail'):
                    return (base.TEXT, getattr(elt, flag))
                node = elt
            if not hasattr(node, b'tag'):
                node = node.getroot()
            if node.tag in ('DOCUMENT_ROOT', 'DOCUMENT_FRAGMENT'):
                return (base.DOCUMENT,)
            else:
                if node.tag == b'<!DOCTYPE>':
                    return (base.DOCTYPE, node.text,
                     node.get(b'publicId'), node.get(b'systemId'))
                else:
                    if node.tag == ElementTreeCommentType:
                        return (base.COMMENT, node.text)
                    assert isinstance(node.tag, string_types), type(node.tag)
                    match = tag_regexp.match(node.tag)
                    if match:
                        namespace, tag = match.groups()
                    else:
                        namespace = None
                        tag = node.tag
                    attrs = OrderedDict()
                    for name, value in list(node.attrib.items()):
                        match = tag_regexp.match(name)
                        if match:
                            attrs[(match.group(1), match.group(2))] = value
                        else:
                            attrs[(None, name)] = value

                    return (
                     base.ELEMENT, namespace, tag,
                     attrs, len(node) or node.text)

                return

        def getFirstChild(self, node):
            if isinstance(node, tuple):
                element, key, parents, flag = node
            else:
                element, key, parents, flag = (
                 node, None, [], None)
            if flag in ('text', 'tail'):
                return
            else:
                if element.text:
                    return (element, key, parents, b'text')
                else:
                    if len(element):
                        parents.append(element)
                        return (
                         element[0], 0, parents, None)
                    return

                return

        def getNextSibling(self, node):
            if isinstance(node, tuple):
                element, key, parents, flag = node
            else:
                return
            if flag == b'text':
                if len(element):
                    parents.append(element)
                    return (
                     element[0], 0, parents, None)
                else:
                    return

            else:
                if element.tail and flag != b'tail':
                    return (element, key, parents, b'tail')
                else:
                    if key < len(parents[(-1)]) - 1:
                        return (parents[(-1)][(key + 1)], key + 1, parents, None)
                    return

            return

        def getParentNode(self, node):
            if isinstance(node, tuple):
                element, key, parents, flag = node
            else:
                return
            if flag == b'text':
                if not parents:
                    return element
                else:
                    return (
                     element, key, parents, None)

            else:
                parent = parents.pop()
                if not parents:
                    return parent
                assert list(parents[(-1)]).count(parent) == 1
                return (parent, list(parents[(-1)]).index(parent), parents, None)
            return

    return locals()


getETreeModule = moduleFactoryFactory(getETreeBuilder)