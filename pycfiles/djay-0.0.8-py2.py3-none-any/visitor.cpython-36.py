# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/jinja2/jinja2/visitor.py
# Compiled at: 2019-07-30 18:47:05
# Size of source mod 2**32: 3316 bytes
"""
    jinja2.visitor
    ~~~~~~~~~~~~~~

    This module implements a visitor for the nodes.

    :copyright: (c) 2017 by the Jinja Team.
    :license: BSD.
"""
from jinja2.nodes import Node

class NodeVisitor(object):
    __doc__ = "Walks the abstract syntax tree and call visitor functions for every\n    node found.  The visitor functions may return values which will be\n    forwarded by the `visit` method.\n\n    Per default the visitor functions for the nodes are ``'visit_'`` +\n    class name of the node.  So a `TryFinally` node visit function would\n    be `visit_TryFinally`.  This behavior can be changed by overriding\n    the `get_visitor` function.  If no visitor function exists for a node\n    (return value `None`) the `generic_visit` visitor is used instead.\n    "

    def get_visitor(self, node):
        """Return the visitor function for this node or `None` if no visitor
        exists for this node.  In that case the generic visit function is
        used instead.
        """
        method = 'visit_' + node.__class__.__name__
        return getattr(self, method, None)

    def visit(self, node, *args, **kwargs):
        """Visit a node."""
        f = self.get_visitor(node)
        if f is not None:
            return f(node, *args, **kwargs)
        else:
            return (self.generic_visit)(node, *args, **kwargs)

    def generic_visit(self, node, *args, **kwargs):
        """Called if no explicit visitor function exists for a node."""
        for node in node.iter_child_nodes():
            (self.visit)(node, *args, **kwargs)


class NodeTransformer(NodeVisitor):
    __doc__ = "Walks the abstract syntax tree and allows modifications of nodes.\n\n    The `NodeTransformer` will walk the AST and use the return value of the\n    visitor functions to replace or remove the old node.  If the return\n    value of the visitor function is `None` the node will be removed\n    from the previous location otherwise it's replaced with the return\n    value.  The return value may be the original node in which case no\n    replacement takes place.\n    "

    def generic_visit(self, node, *args, **kwargs):
        for field, old_value in node.iter_fields():
            if isinstance(old_value, list):
                new_values = []
                for value in old_value:
                    if isinstance(value, Node):
                        value = (self.visit)(value, *args, **kwargs)
                        if value is None:
                            continue
                        elif not isinstance(value, Node):
                            new_values.extend(value)
                            continue
                    new_values.append(value)

                old_value[:] = new_values
            else:
                if isinstance(old_value, Node):
                    new_node = (self.visit)(old_value, *args, **kwargs)
                    if new_node is None:
                        delattr(node, field)
                    else:
                        setattr(node, field, new_node)

        return node

    def visit_list(self, node, *args, **kwargs):
        """As transformers may return lists in some places this method
        can be used to enforce a list as return value.
        """
        rv = (self.visit)(node, *args, **kwargs)
        if not isinstance(rv, list):
            rv = [
             rv]
        return rv