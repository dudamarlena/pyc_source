# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/dist-packages/luqum/utils.py
# Compiled at: 2018-06-13 04:22:04
# Size of source mod 2**32: 11577 bytes
"""Various utilities for dealing with syntax trees.

Include base classes to implement a visitor pattern.

"""
from .tree import BaseOperation, OrOperation, AndOperation

def camel_to_lower(name):
    return ''.join((('_' + w.lower() if w.isupper() else w.lower()) for w in name)).lstrip('_')


class LuceneTreeVisitor:
    __doc__ = "\n    Tree Visitor base class, inspired by python's :class:`ast.NodeVisitor`.\n\n    This class is meant to be subclassed, with the subclass implementing\n    visitor methods for each Node type it is interested in.\n\n    By default, those visitor method should be named ``'visit_'`` + class\n    name of the node, converted to lower_case (ie: visit_search_node for a\n    SearchNode class).\n\n    You can tweak this behaviour by overriding the `visitor_method_prefix` &\n    `generic_visitor_method_name` class attributes.\n\n    If the goal is to modify the initial tree,\n    use :py:class:`LuceneTreeTranformer` instead.\n    "
    visitor_method_prefix = 'visit_'
    generic_visitor_method_name = 'generic_visit'
    _get_method_cache = None

    def _get_method(self, node):
        if self._get_method_cache is None:
            self._get_method_cache = {}
        try:
            meth = self._get_method_cache[type(node)]
        except KeyError:
            for cls in node.__class__.mro():
                try:
                    method_name = '{}{}'.format(self.visitor_method_prefix, camel_to_lower(cls.__name__))
                    meth = getattr(self, method_name)
                    break
                except AttributeError:
                    continue

            else:
                meth = getattr(self, self.generic_visitor_method_name)

            self._get_method_cache[type(node)] = meth

        return meth

    def visit(self, node, parents=None):
        """ Basic, recursive traversal of the tree. """
        parents = parents or []
        method = self._get_method(node)
        yield from method(node, parents)
        for child in node.children:
            yield from self.visit(child, parents + [node])

        if False:
            yield None

    def generic_visit(self, node, parents=None):
        """
        Default visitor function, called if nothing matches the current node.
        """
        return iter([])


class LuceneTreeTransformer(LuceneTreeVisitor):
    __doc__ = '\n    A :class:`LuceneTreeVisitor` subclass that walks the abstract syntax tree\n    and allows modifications of traversed nodes.\n\n    The `LuceneTreeTransormer` will walk the AST and use the return value of the\n    visitor methods to replace or remove the old node. If the return value of\n    the visitor method is ``None``, the node will be removed from its location,\n    otherwise it is replaced with the return value. The return value may be the\n    original node, in which case no replacement takes place.\n    '

    def replace_node(self, old_node, new_node, parent):
        for k, v in parent.__dict__.items():
            if v == old_node:
                parent.__dict__[k] = new_node
                break
            else:
                if isinstance(v, list):
                    try:
                        i = v.index(old_node)
                        if new_node is None:
                            del v[i]
                        else:
                            v[i] = new_node
                        break
                    except ValueError:
                        pass

    def generic_visit(self, node, parent=None):
        return node

    def visit(self, node, parents=None):
        """
        Recursively traverses the tree and replace nodes with the appropriate
        visitor method's return values.
        """
        parents = parents or []
        method = self._get_method(node)
        new_node = method(node, parents)
        if parents:
            self.replace_node(node, new_node, parents[(-1)])
        node = new_node
        if node is not None:
            for child in node.children:
                self.visit(child, parents + [node])

        return node


class LuceneTreeVisitorV2(LuceneTreeVisitor):
    __doc__ = "\n    V2 of the LuceneTreeVisitor allowing to evaluate the AST\n\n    It differs from py:cls:`LuceneTreeVisitor`\n    because it's up to the visit method to recursively call children (or not)\n\n    This class is meant to be subclassed, with the subclass implementing\n    visitor methods for each Node type it is interested in.\n\n    By default, those visitor method should be named ``'visit_'`` + class\n    name of the node, converted to lower_case (ie: visit_search_node for a\n    SearchNode class).\n\n    You can tweak this behaviour by overriding the `visitor_method_prefix` &\n    `generic_visitor_method_name` class attributes.\n\n    If the goal is to modify the initial tree,\n    use :py:class:`LuceneTreeTranformer` instead.\n    "

    def visit(self, node, parents=None, context=None):
        """ Basic, recursive traversal of the tree.

        :param list parents: the list of parents
        :parma dict context: a dict of contextual variable for free use
          to track states while traversing the tree
        """
        if parents is None:
            parents = []
        method = self._get_method(node)
        return method(node, parents, context)

    def generic_visit(self, node, parents=None, context=None):
        """
        Default visitor function, called if nothing matches the current node.
        """
        raise AttributeError('No visitor found for this type of node: {}'.format(node.__class__))


class UnknownOperationResolver(LuceneTreeTransformer):
    __doc__ = 'Transform the UnknownOperation to OR or AND\n    '
    VALID_OPERATIONS = frozenset([None, AndOperation, OrOperation])
    DEFAULT_OPERATION = AndOperation

    def __init__(self, resolve_to=None):
        """Initialize a new resolver

        :param resolve_to: must be either None, OrOperation or AndOperation.

          for the latter two the UnknownOperation is repalced by specified operation.

          if it is None, we use the last operation encountered, as would Lucene do
        """
        if resolve_to not in self.VALID_OPERATIONS:
            raise ValueError('%r is not a valid value for resolve_to' % resolve_to)
        self.resolve_to = resolve_to
        self.last_operation = {}

    def _first_nonop_parent(self, parents):
        for parent in parents:
            if not isinstance(parent, BaseOperation):
                return id(parent)

    def visit_or_operation(self, node, parents=None):
        if self.resolve_to is None:
            parent = self._first_nonop_parent(parents)
            self.last_operation[parent] = OrOperation
        return node

    def visit_and_operation(self, node, parents=None):
        if self.resolve_to is None:
            parent = self._first_nonop_parent(parents)
            self.last_operation[parent] = AndOperation
        return node

    def visit_unknown_operation(self, node, parents=None):
        if self.resolve_to is None:
            parent = self._first_nonop_parent(parents)
            operation = self.last_operation.get(parent, None)
            if operation is None:
                operation = self.DEFAULT_OPERATION
        else:
            operation = self.resolve_to
        return operation(*node.operands)

    def __call__(self, tree):
        return self.visit(tree)


def normalize_nested_fields_specs(nested_fields):
    """normalize nested_fields specification to only have nested dicts

    :param dict nested_fields:  dict contains fields that are nested in ES
        each nested fields contains either
        a dict of nested fields
        (if some of them are also nested)
        or a list of nesdted fields (this is for commodity)

    ::
        >>> from unittest import TestCase
        >>> TestCase().assertDictEqual(
        ...     normalize_nested_fields_specs(
        ...         {"author" : {"books": ["name", "ref"], "firstname" : None }}),
        ...     {"author" : {"books": {"name": {}, "ref": {}}, "firstname" : {} }})
    """
    if nested_fields is None:
        return {}
    if isinstance(nested_fields, dict):
        return {k:normalize_nested_fields_specs(v) for k, v in nested_fields.items()}
    return {sub:{} for sub in nested_fields}


def _flatten_fields_specs(object_fields):
    if not object_fields:
        return [[]]
    if isinstance(object_fields, dict):
        return [[k] + v2 for k, v in object_fields.items() for v2 in _flatten_fields_specs(v)]
    return [[k] for k in object_fields]


def flatten_nested_fields_specs(nested_fields):
    """normalize object_fields specification to only have a simple set

    :param dict nested_fields:  contains fields that are object in ES
        has a serie of nested dict.
        List are accepted as well for concisness.

    ::
        >>> from unittest import TestCase
        >>> flatten_nested_fields_specs(None)
        set()
        >>> TestCase().assertEqual(
        ...     flatten_nested_fields_specs(["author.name", "book.title"]),
        ...     set(["author.name", "book.title"]))
        >>> TestCase().assertEqual(
        ...     flatten_nested_fields_specs(
        ...         {"book" : { "author": ["firstname", "lastname"], "title" : None }}),
        ...     set(["book.author.firstname", "book.author.lastname", "book.title"]))
    """
    if isinstance(nested_fields, dict):
        return set(('.'.join(v) for v in _flatten_fields_specs(nested_fields)))
    if nested_fields is None:
        return set([])
    return set(nested_fields)


def normalize_object_fields_specs(object_fields):
    """normalize object_fields specification to only have a simple set

    :param dict object_fields:  contains fields that are object in ES
        has a serie of nested dict.
        List are accepted as well for concisness.
        None, which means no spec, is returned as is.

    ::
        >>> from unittest import TestCase
        >>> normalize_object_fields_specs(None) is None
        True
        >>> TestCase().assertEqual(
        ...     normalize_object_fields_specs(["author.name", "book.title"]),
        ...     set(["author.name", "book.title"]))
        >>> TestCase().assertEqual(
        ...     normalize_object_fields_specs(
        ...         {"book" : { "author": ["firstname", "lastname"], "title" : None }}),
        ...     set(["book.author.firstname", "book.author.lastname", "book.title"]))
    """
    if object_fields is None:
        return
    if isinstance(object_fields, dict):
        return set(('.'.join(v) for v in _flatten_fields_specs(object_fields)))
    return set(object_fields)