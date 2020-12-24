# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/dist-packages/luqum/tree.py
# Compiled at: 2018-10-25 11:52:49
# Size of source mod 2**32: 9524 bytes
"""Elements that will constitute the parse tree of a query.

You may use these items to build a tree representing a query,
or get a tree as the result of parsing a query string.
"""
import re
from decimal import Decimal
_MARKER = object()

class Item(object):
    __doc__ = 'Base class for all items that compose the parse tree.\n\n    An item is a part of a request.\n    '
    _equality_attrs = []

    @property
    def children(self):
        """As base of a tree structure, an item may have children"""
        return []

    def __repr__(self):
        children = ', '.join((c.__repr__() for c in self.children))
        return '%s(%s)' % (self.__class__.__name__, children)

    def __eq__(self, other):
        """a basic equal operation
        """
        return self.__class__ == other.__class__ and len(self.children) == len(other.children) and all((getattr(self, a, _MARKER) == getattr(other, a, _MARKER) for a in self._equality_attrs)) and all((c.__eq__(d) for c, d in zip(self.children, other.children)))


class SearchField(Item):
    __doc__ = 'Indicate wich field the search expression operates on\n\n    eg: *desc* in ``desc:(this OR that)``\n\n    :param str name: name of the field\n    :param expr: the searched expression\n    '
    _equality_attrs = ['name']

    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def __str__(self):
        return self.name + ':' + self.expr.__str__()

    def __repr__(self):
        return 'SearchField(%r, %s)' % (self.name, self.expr.__repr__())

    @property
    def children(self):
        """the only child is the expression"""
        return [
         self.expr]


class BaseGroup(Item):
    __doc__ = 'Base class for group of expressions or field values\n\n    :param expr: the expression inside parenthesis\n    '

    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return '(%s)' % self.expr.__str__()

    @property
    def children(self):
        """the only child is the expression"""
        return [
         self.expr]


class Group(BaseGroup):
    __doc__ = 'Group sub expressions\n    '


class FieldGroup(BaseGroup):
    __doc__ = 'Group values for a query on a field\n    '


def group_to_fieldgroup(g):
    return FieldGroup(g.expr)


class Range(Item):
    __doc__ = 'A Range\n\n    :param low: lower bound\n    :param high: higher bound\n    :param bool include_low: wether lower bound is included\n    :param bool include_high: wether higher bound is included\n    '
    LOW_CHAR = {True:'[', 
     False:'{'}
    HIGH_CHAR = {True:']',  False:'}'}

    def __init__(self, low, high, include_low=True, include_high=True):
        self.low = low
        self.high = high
        self.include_low = include_low
        self.include_high = include_high

    @property
    def children(self):
        """children are lower and higher bound expressions"""
        return [
         self.low, self.high]

    def __str__(self):
        return '%s%s TO %s%s' % (
         self.LOW_CHAR[self.include_low],
         self.low.__str__(),
         self.high.__str__(),
         self.HIGH_CHAR[self.include_high])


class Term(Item):
    __doc__ = 'Base for terms\n\n    :param str value: the value\n    '
    WILDCARDS_PATTERN = re.compile('((?<=[^\\\\])[?*]|^[?*])')
    WORD_ESCAPED_CHARS = re.compile('\\\\([+\\-&|!(){}[\\]^"~*?:\\\\])')
    _equality_attrs = [
     'value']

    def __init__(self, value):
        self.value = value

    @property
    def unescaped_value(self):
        return self.WORD_ESCAPED_CHARS.sub('\\1', self.value)

    def is_wildcard(self):
        """:return bool: True if value is the wildcard ``*``
        """
        return self.value == '*'

    def iter_wildcards(self):
        """list wildcards contained in value and their positions
        """
        for matched in self.WILDCARDS_PATTERN.finditer(self.value):
            yield (
             matched.span(), matched.group())

    def split_wildcards(self):
        """split term on wildcards
        """
        return self.WILDCARDS_PATTERN.split(self.value)

    def has_wildcard(self):
        """:return bool: True if value contains a wildcards
        """
        return any(self.iter_wildcards())

    def __str__(self):
        return self.value

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, str(self))


class Word(Term):
    __doc__ = 'A single word term\n\n    :param str value: the value\n    '


class Phrase(Term):
    __doc__ = 'A phrase term, that is a sequence of words enclose in quotes\n\n    :param str value: the value, including the quotes. Eg. ``\'"my phrase"\'``\n    '

    def __init__(self, value):
        super(Phrase, self).__init__(value)
        if not (self.value.endswith('"') and self.value.startswith('"')):
            raise AssertionError('Phrase value must contain the quotes')


class BaseApprox(Item):
    __doc__ = 'Base for approximations, that is fuzziness and proximity\n    '
    _equality_attrs = ['term', 'degree']

    def __repr__(self):
        return '%s(%s, %s)' % (self.__class__.__name__, self.term.__repr__(), self.degree)

    @property
    def children(self):
        return [self.term]


class Fuzzy(BaseApprox):
    __doc__ = 'Fuzzy search on word\n\n    :param Word term: the approximated term\n    :param degree: the degree which will be converted to :py:class:`decimal.Decimal`.\n    '

    def __init__(self, term, degree=None):
        self.term = term
        if degree is None:
            degree = 0.5
        self.degree = Decimal(degree).normalize()

    def __str__(self):
        return '%s~%s' % (self.term, self.degree)


class Proximity(BaseApprox):
    __doc__ = 'Proximity search on phrase\n\n    :param Phrase term: the approximated phrase\n    :param degree: the degree which will be converted to :py:func:`int`.\n    '

    def __init__(self, term, degree=None):
        self.term = term
        if degree is None:
            degree = 1
        self.degree = int(degree)

    def __str__(self):
        return '%s~' % self.term + ('%d' % self.degree if self.degree is not None else '')


class Boost(Item):
    __doc__ = 'A term for boosting a value or a group there of\n\n    :param expr: the boosted expression\n    :param force: boosting force, will be converted to :py:class:`decimal.Decimal`\n    '

    def __init__(self, expr, force):
        self.expr = expr
        self.force = Decimal(force).normalize()

    @property
    def children(self):
        """The only child is the boosted expression
        """
        return [
         self.expr]

    def __str__(self):
        return '%s^%s' % (self.expr.__str__(), self.force)


class BaseOperation(Item):
    __doc__ = '\n    Parent class for binary operations are binary operation used to join expressions,\n    like OR and AND\n\n    :param operands: expressions to apply operation on\n    '

    def __init__(self, *operands):
        self.operands = operands

    def __str__(self):
        return (' %s ' % self.op).join((str(o) for o in self.operands))

    @property
    def children(self):
        """children are left and right expressions
        """
        return self.operands


class UnknownOperation(BaseOperation):
    __doc__ = 'Unknown Boolean operator.\n\n    .. warning::\n        This is used to represent implicit operations (ie: term:foo term:bar),\n        as we cannot know for sure which operator should be used.\n\n        Lucene seem to use whatever operator was used before reaching that one,\n        defaulting to AND, but we cannot know anything about this at parsing\n        time...\n    .. seealso::\n        the :py:class:`.utils.UnknownOperationResolver` to resolve those nodes to OR and AND\n    '
    op = ''

    def __str__(self):
        return ' '.join((str(o) for o in self.operands))


class OrOperation(BaseOperation):
    __doc__ = 'OR expression\n    '
    op = 'OR'


class AndOperation(BaseOperation):
    __doc__ = 'AND expression\n    '
    op = 'AND'


def create_operation(cls, a, b):
    """Create operation between a and b, merging if a or b is already an operation of same class
    """
    operands = []
    operands.extend(a.operands if isinstance(a, cls) else [a])
    operands.extend(b.operands if isinstance(b, cls) else [b])
    return cls(*operands)


class Unary(Item):
    __doc__ = 'Parent class for unary operations\n\n    :param a: the expression the operator applies on\n    '

    def __init__(self, a):
        self.a = a

    def __str__(self):
        return '%s%s' % (self.op, self.a.__str__())

    @property
    def children(self):
        return [self.a]


class Plus(Unary):
    __doc__ = 'plus, unary operation\n    '
    op = '+'


class Not(Unary):
    op = 'NOT '


class Prohibit(Unary):
    __doc__ = 'The negation\n    '
    op = '-'