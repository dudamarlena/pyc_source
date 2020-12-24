# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rsutton/workarea/env/eulxml/lib/python2.7/site-packages/eulxml/xpath/ast.py
# Compiled at: 2016-05-23 17:04:57
"""Abstract Syntax Tree nodes for parsed XPath.

This module contains basic nodes for representing parsed XPath expressions.
The parser provided by this module creates its parsed XPath representation
from the classes defined in this module. Library callers will mostly not use
this module directly, unless they need to produce XPath ASTs from scratch or
perhaps introspect ASTs returned by the parser.
"""
from __future__ import unicode_literals
import sys
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
if PY3:
    string_types = str
else:
    string_types = basestring
__all__ = [
 b'serialize',
 b'UnaryExpression',
 b'BinaryExpression',
 b'PredicatedExpression',
 b'AbsolutePath',
 b'Step',
 b'NameTest',
 b'NodeType',
 b'AbbreviatedStep',
 b'VariableReference',
 b'FunctionCall']

def serialize(xp_ast):
    """Serialize an XPath AST as a valid XPath expression."""
    return (b'').join(_serialize(xp_ast))


def _serialize(xp_ast):
    """Generate token strings which, when joined together, form a valid
    XPath serialization of the AST."""
    if hasattr(xp_ast, b'_serialize'):
        for tok in xp_ast._serialize():
            yield tok

    elif isinstance(xp_ast, string_types):
        yield repr(xp_ast).lstrip(b'u')
    else:
        yield str(xp_ast)


class UnaryExpression(object):
    """A unary XPath expression. Practially, this means -foo."""

    def __init__(self, op, right):
        self.op = op
        self.right = right

    def __repr__(self):
        return b'<%s %s %s>' % (self.__class__.__name__,
         self.op, serialize(self.right))

    def _serialize(self):
        yield self.op
        for tok in _serialize(self.right):
            yield tok


KEYWORDS = set([b'or', b'and', b'div', b'mod'])

class BinaryExpression(object):
    """Any binary XPath expression. a/b; a and b; a | b."""

    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return b'<%s %s %s %s>' % (self.__class__.__name__,
         serialize(self.left), self.op, serialize(self.right))

    def _serialize(self):
        for tok in _serialize(self.left):
            yield tok

        if self.op in KEYWORDS:
            yield b' '
            yield self.op
            yield b' '
        else:
            yield self.op
        for tok in _serialize(self.right):
            yield tok


class PredicatedExpression(object):
    """A filtered XPath expression. $var[1]; (a or b)[foo][@bar]."""

    def __init__(self, base, predicates=None):
        self.base = base
        self.predicates = predicates or []

    def __repr__(self):
        return b'<%s %s>' % (self.__class__.__name__,
         serialize(self))

    def append_predicate(self, pred):
        self.predicates.append(pred)

    def _serialize(self):
        yield b'('
        for tok in _serialize(self.base):
            yield tok

        yield b')'
        for pred in self.predicates:
            yield b'['
            for tok in _serialize(pred):
                yield tok

            yield b']'


class AbsolutePath(object):
    """An absolute XPath path. /a/b/c; //a/ancestor:b/@c."""

    def __init__(self, op=b'/', relative=None):
        self.op = op
        self.relative = relative

    def __repr__(self):
        if self.relative:
            return b'<%s %s %s>' % (self.__class__.__name__,
             self.op, serialize(self.relative))
        else:
            return b'<%s %s>' % (self.__class__.__name__, self.op)

    def _serialize(self):
        yield self.op
        for tok in _serialize(self.relative):
            yield tok


class Step(object):
    """A single step in a relative path. a; @b; text(); parent::foo:bar[5]."""

    def __init__(self, axis, node_test, predicates):
        self.axis = axis
        self.node_test = node_test
        self.predicates = predicates

    def __repr__(self):
        return b'<%s %s>' % (self.__class__.__name__,
         serialize(self))

    def _serialize(self):
        if self.axis == b'@':
            yield b'@'
        else:
            if self.axis:
                yield self.axis
                yield b'::'
            for tok in self.node_test._serialize():
                yield tok

            for predicate in self.predicates:
                yield b'['
                for tok in _serialize(predicate):
                    yield tok

                yield b']'


class NameTest(object):
    """An element name node test for a Step."""

    def __init__(self, prefix, name):
        self.prefix = prefix
        self.name = name

    def __repr__(self):
        return b'<%s %s>' % (self.__class__.__name__,
         serialize(self))

    def _serialize(self):
        if self.prefix:
            yield self.prefix
            yield b':'
        yield self.name

    def __str__(self):
        return (b'').join(self._serialize())


class NodeType(object):
    """A node type node test for a Step."""

    def __init__(self, name, literal=None):
        self.name = name
        self.literal = literal

    def __repr__(self):
        return b'<%s %s>' % (self.__class__.__name__,
         serialize(self))

    def _serialize(self):
        yield self.name
        yield b'('
        if self.literal is not None:
            for tok in _serialize(self.literal):
                yield self.literal

        yield b')'
        return

    def __str__(self):
        return (b'').join(self._serialize())


class AbbreviatedStep(object):
    """An abbreviated XPath step. . or .."""

    def __init__(self, abbr):
        self.abbr = abbr

    def __repr__(self):
        return b'<%s %s>' % (self.__class__.__name__,
         serialize(self))

    def _serialize(self):
        yield self.abbr


class VariableReference(object):
    """An XPath variable reference. $foo; $myns:foo."""

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return b'<%s %s>' % (self.__class__.__name__,
         serialize(self))

    def _serialize(self):
        yield b'$'
        prefix, localname = self.name
        if prefix:
            yield prefix
            yield b':'
        yield localname


class FunctionCall(object):
    """An XPath function call. foo(); my:foo(1); foo(1, 'a', $var)."""

    def __init__(self, prefix, name, args):
        self.prefix = prefix
        self.name = name
        self.args = args

    def __repr__(self):
        return b'<%s %s>' % (self.__class__.__name__,
         serialize(self))

    def _serialize(self):
        if self.prefix:
            yield self.prefix
            yield b':'
        yield self.name
        yield b'('
        if self.args:
            for tok in _serialize(self.args[0]):
                yield tok

            for arg in self.args[1:]:
                yield b','
                for tok in _serialize(arg):
                    yield tok

        yield b')'