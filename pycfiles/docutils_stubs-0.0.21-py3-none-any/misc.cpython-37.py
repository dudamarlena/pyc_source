# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tkomiya/work/sphinx/.tox/py37/lib/python3.7/site-packages/docutils/transforms/misc.py
# Compiled at: 2018-11-25 06:19:18
# Size of source mod 2**32: 4882 bytes
"""
Miscellaneous transforms.
"""
__docformat__ = 'reStructuredText'
from docutils import nodes
from docutils.transforms import Transform, TransformError

class CallBack(Transform):
    __doc__ = "\n    Inserts a callback into a document.  The callback is called when the\n    transform is applied, which is determined by its priority.\n\n    For use with `nodes.pending` elements.  Requires a ``details['callback']``\n    entry, a bound method or function which takes one parameter: the pending\n    node.  Other data can be stored in the ``details`` attribute or in the\n    object hosting the callback method.\n    "
    default_priority = 990

    def apply(self):
        pending = self.startnode
        pending.details['callback'](pending)
        pending.parent.remove(pending)


class ClassAttribute(Transform):
    __doc__ = '\n    Move the "class" attribute specified in the "pending" node into the\n    immediately following non-comment element.\n    '
    default_priority = 210

    def apply(self):
        pending = self.startnode
        parent = pending.parent
        child = pending
        while parent:
            for index in range(parent.index(child) + 1, len(parent)):
                element = parent[index]
                if isinstance(element, nodes.Invisible) or isinstance(element, nodes.system_message):
                    continue
                element['classes'] += pending.details['class']
                pending.parent.remove(pending)
                return
            else:
                child = parent
                parent = parent.parent

        error = self.document.reporter.error(('No suitable element following "%s" directive' % pending.details['directive']),
          (nodes.literal_block(pending.rawsource, pending.rawsource)),
          line=(pending.line))
        pending.replace_self(error)


class Transitions(Transform):
    __doc__ = '\n    Move transitions at the end of sections up the tree.  Complain\n    on transitions after a title, at the beginning or end of the\n    document, and after another transition.\n\n    For example, transform this::\n\n        <section>\n            ...\n            <transition>\n        <section>\n            ...\n\n    into this::\n\n        <section>\n            ...\n        <transition>\n        <section>\n            ...\n    '
    default_priority = 830

    def apply(self):
        for node in self.document.traverse(nodes.transition):
            self.visit_transition(node)

    def visit_transition(self, node):
        index = node.parent.index(node)
        error = None
        if not index == 0:
            if isinstance(node.parent[0], nodes.title) and not index == 1:
                if not isinstance(node.parent[1], nodes.subtitle) or index == 2:
                    if not isinstance(node.parent, nodes.document):
                        assert isinstance(node.parent, nodes.section)
                    error = self.document.reporter.error('Document or section may not begin with a transition.',
                      source=(node.source),
                      line=(node.line))
        elif isinstance(node.parent[(index - 1)], nodes.transition):
            error = self.document.reporter.error('At least one body element must separate transitions; adjacent transitions are not allowed.',
              source=(node.source),
              line=(node.line))
        if error:
            node.parent.insert(index, error)
            index += 1
        assert index < len(node.parent)
        if index != len(node.parent) - 1:
            return
        sibling = node
        while index == len(sibling.parent) - 1:
            sibling = sibling.parent
            if sibling.parent is None:
                error = self.document.reporter.error('Document may not end with a transition.',
                  line=(node.line))
                node.parent.insert(node.parent.index(node) + 1, error)
                return
            index = sibling.parent.index(sibling)

        node.parent.remove(node)
        sibling.parent.insert(index + 1, node)