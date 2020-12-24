# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\xpath\Axis.py
# Compiled at: 2018-01-18 12:33:29
# Size of source mod 2**32: 7877 bytes
import logging
from .NodeTest import NodeTest
from .Predicate import Predicate
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Axis(object):

    def a_ancestor(node):
        ns = []
        while node._parent is not None:
            ns.append(node._parent)
            node = node._parent

        return ns

    def a_ancestor_or_self(node):
        ns = [
         node]
        ns.extend(Axis.a_ancestor(node))
        return ns

    def a_attribute(node):
        if hasattr(node, 'attribute_nodes'):
            return list(node.attribute_nodes.values())
        else:
            return []

    def a_child(node):
        if hasattr(node, 'children'):
            return node.children.copy()
        else:
            return []

    def a_descendant(node):
        logger.debug('Collecting descendants of ' + str(node))
        if not hasattr(node, 'children') or len(node.children) == 0:
            logger.debug(str(node) + ' has no children')
            return []
        else:
            ns = []
            for n in node.children:
                ns.append(n)
                ns.extend(Axis.a_descendant(n))

            logger.debug(str(node) + ' descendants: [' + ','.join([str(x) for x in ns]) + ']')
            return ns

    def a_descendant_or_self(node):
        ns = [node]
        ns.extend(Axis.a_descendant(node))
        return ns

    def a_namespace(node):
        if hasattr(node, 'namespace_nodes'):
            return list(node.namespace_nodes.values())
        else:
            return []

    def a_parent(node):
        if node._parent is not None:
            return [node._parent]
        else:
            return []

    def a_following_sibling(node):
        from ..Attribute import Attribute
        from ..Namespace import Namespace
        if isinstance(node, Attribute) or isinstance(node, Namespace) or node._parent is None:
            return []
        else:
            ns = []
            node_i = node._parent.children.index(node) + 1
            for n in node._parent.children[node_i:]:
                ns.append(n)

            return ns

    def a_following(node):
        from ..Attribute import Attribute
        from ..Namespace import Namespace
        if isinstance(node, Attribute) or isinstance(node, Namespace):
            return []
        else:
            ns = []
            while node is not None:
                ns.extend(Axis.a_following_sibling(node))
                node = node._parent

            return ns

    def a_preceding_sibling(node):
        from ..Attribute import Attribute
        from ..Namespace import Namespace
        if isinstance(node, Attribute) or isinstance(node, Namespace) or node._parent is None:
            return []
        else:
            ns = []
            node_i = node._parent.children.index(node)
            for n in reversed(node._parent.children[:node_i]):
                ns.append(n)

            return ns

    def a_preceding(node):
        from ..Attribute import Attribute
        from ..Namespace import Namespace
        if isinstance(node, Attribute) or isinstance(node, Namespace):
            return []
        else:
            ns = []
            while node is not None:
                logger.debug('Extending nodeset with ' + str(node) + ' preceding siblings')
                ns.extend(Axis.a_preceding_sibling(node))
                if node._parent is not None:
                    logger.debug('Appending parent of ' + str(node) + ': ' + str(node._parent))
                    ns.append(node._parent)
                node = node._parent

            return ns

    AXES = {'ancestor':a_ancestor, 
     'ancestor-or-self':a_ancestor_or_self, 
     'attribute':a_attribute, 
     'child':a_child, 
     'descendant':a_descendant, 
     'descendant-or-self':a_descendant_or_self, 
     'following':a_following, 
     'following-sibling':a_following_sibling, 
     'namespace':a_namespace, 
     'parent':a_parent, 
     'preceding':a_preceding, 
     'preceding-sibling':a_preceding_sibling, 
     'self':lambda node: [
      node]}
    PRINCIPAL_NODE_TYPE = {'ancestor':'element', 
     'ancestor-or-self':'element', 
     'attribute':'attribute', 
     'child':'element', 
     'descendant':'element', 
     'descendant-or-self':'element', 
     'following':'element', 
     'following-sibling':'element', 
     'namespace':'namespace', 
     'parent':'element', 
     'preceding':'element', 
     'preceding-sibling':'element', 
     'self':'element'}
    AXIS_DIRECTION = {'ancestor':'reverse', 
     'ancestor-or-self':'reverse', 
     'attribute':'forward', 
     'child':'forward', 
     'descendant':'forward', 
     'descendant-or-self':'forward', 
     'following':'forward', 
     'following-sibling':'forward', 
     'namespace':'forward', 
     'parent':'forward', 
     'preceding':'reverse', 
     'preceding-sibling':'reverse', 
     'self':'forward'}

    def __init__(self, name):
        self.name = name
        self.children = []

    def evaluate(self, context_node, context_position, context_size, variables):
        from ..Document import Document
        if len(self.children) <= 0:
            raise ValueError('Axis missing NodeTest')
        for i, child in enumerate(self.children):
            if i == 0 and not isinstance(child, NodeTest):
                raise ValueError('Axis missing NodeTest')
            else:
                if i > 0 and not isinstance(child, Predicate):
                    raise ValueError('Axis children past the first must be predicates: ' + str(child))

        nodeset = Axis.AXES[self.name](context_node)
        if len(nodeset) == 0:
            return nodeset
        else:
            logger.debug('Initial nodeset: [' + ','.join([str(x) for x in nodeset]) + ']')
            for c in self.children:
                ns = []
                for i, n in enumerate(nodeset):
                    if c.evaluate(n, i + 1, len(nodeset), variables):
                        ns.append(n)

                nodeset = ns

            if Axis.AXIS_DIRECTION[self.name] == 'forward':
                nodeset = Document.order_sort(nodeset)
            else:
                nodeset = Document.order_sort(nodeset, reverse=True)
            logger.debug('Final nodeset: [' + ','.join([str(x) for x in nodeset]) + ']')
            return nodeset

    def get_principal_node_type(self):
        return Axis.PRINCIPAL_NODE_TYPE[self.name]

    def __str__(self):
        return 'Axis ' + hex(id(self)) + ' ' + self.name + ': [' + ','.join([str(x) for x in self.children]) + ']'