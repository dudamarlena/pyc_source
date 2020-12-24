# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/slimit/slimit/visitors/nodevisitor.py
# Compiled at: 2018-07-11 18:15:31
__author__ = 'Ruslan Spivak <ruslan.spivak@gmail.com>'

class ASTVisitor(object):
    """Base class for custom AST node visitors.

    Example:

    >>> from slimit.parser import Parser
    >>> from slimit.visitors.nodevisitor import ASTVisitor
    >>>
    >>> text = '''
    ... var x = {
    ...     "key1": "value1",
    ...     "key2": "value2"
    ... };
    ... '''
    >>>
    >>> class MyVisitor(ASTVisitor):
    ...     def visit_Object(self, node):
    ...         '''Visit object literal.'''
    ...         for prop in node:
    ...             left, right = prop.left, prop.right
    ...             print 'Property value: %s' % right.value
    ...             # visit all children in turn
    ...             self.visit(prop)
    ...
    >>>
    >>> parser = Parser()
    >>> tree = parser.parse(text)
    >>> visitor = MyVisitor()
    >>> visitor.visit(tree)
    Property value: "value1"
    Property value: "value2"

    """

    def visit(self, node):
        method = 'visit_%s' % node.__class__.__name__
        return getattr(self, method, self.generic_visit)(node)

    def generic_visit(self, node):
        for child in node:
            self.visit(child)


class NodeVisitor(object):
    """Simple node visitor."""

    def visit(self, node):
        """Returns a generator that walks all children recursively."""
        for child in node:
            yield child
            for subchild in self.visit(child):
                yield subchild


def visit(node):
    visitor = NodeVisitor()
    for child in visitor.visit(node):
        yield child