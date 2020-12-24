# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/llb3d/ast.py
# Compiled at: 2019-01-14 10:33:28
# Size of source mod 2**32: 5810 bytes
"""Ast for llb3d."""
import collections
from typing import Tuple
from textwrap import indent
from inspect import signature
from typeguard import typechecked
IDENT = 2

class FrozenDict(collections.Mapping):
    __doc__ = 'Frozen dict.'

    def __init__(self, **kwargs):
        """Initialize self.  See help(type(self)) for accurate signature."""
        self._dict = dict(**kwargs)
        self._hash = 0
        for pair in self.items():
            self._hash ^= hash(pair)

    def __iter__(self):
        """Implement iter(self)."""
        return iter(self._dict)

    def __len__(self) -> int:
        """Implement len(self)."""
        return len(self._dict)

    def __getitem__(self, key):
        """Implement self[key]."""
        return self._dict[key]

    def __hash__(self) -> int:
        """Implement hash(self)."""
        return self._hash

    def __eq__(self, other) -> bool:
        """Return self==other."""
        if type(self) is not type(other) or hash(self) != hash(other):
            return False
        else:
            return self._dict == other._dict

    @typechecked
    def __getattr__(self, name: str):
        """Return name from dict."""
        return self._dict[name]


class Statement(FrozenDict):
    __doc__ = 'Basic statement.\n\n    Frozen dict, that can be printed.\n\n    >>> expr = Statement("Hello, {name}!", name=\'Alice\')\n    >>> expr[\'name\']\n    \'Alice\'\n    >>> str(expr)\n    \'Hello, Alice!\'\n    '

    def __init__(self, format_str, **kwds):
        (super().__init__)(**kwds)
        self._hash ^= hash(format_str) ^ hash(type(self))
        self._format_str = format_str

    def __str__(self) -> str:
        """Implement str(self)."""
        return (self._format_str.format)(**self)

    def __repr__(self) -> str:
        """Implemet repr(self)."""
        sig = signature(type(self).__init__)
        params = tuple(sig.parameters.keys())
        params_str = ', '.join(repr(self[c]) for c in params[1:])
        return '{cls}({params_str})'.format(cls=(type(self).__name__),
          params_str=params_str)


class Expression(Statement):
    __doc__ = 'Basic expression.'


class Identifier(Expression):
    __doc__ = "Identifier for variable or function.\n\n    >>> alice = Identifier('Alice')\n    >>> alice['name']\n    'Alice'\n    >>> str(alice)\n    'Alice'\n    "

    @typechecked
    def __init__(self, name):
        """Initialize self.  See help(type(self)) for accurate signature."""
        super().__init__('{name}', name=name)


class Literal(Expression):
    __doc__ = 'Abstract literal.'

    def __init__(self, value):
        super().__init__('{value}', value=value)


class IntLiteral(Literal):
    __doc__ = 'Integer literal.\n\n    Integer values are numeric values with no fractional part in them.\n    For example: 5, -10, 0 are integer values.\n    All integer values in your program must be in the range -2147483648\n    to +2147483647 (int32).\n    '

    @typechecked
    def __init__(self, value):
        """Initialize self.  See help(type(self)) for accurate signature."""
        super().__init__(value)


class FloatLiteral(Literal):
    __doc__ = 'Float literal.\n\n    Floating point values are numeric values that include a fractional part.\n    For example: .5, -10.1, 0.0 are all floating point values (float32).\n    '

    @typechecked
    def __init__(self, value):
        """Initialize self.  See help(type(self)) for accurate signature."""
        super().__init__(value)


class StrLiteral(Literal):
    __doc__ = 'String literal.\n\n    Strings values are used to contain text. For example: "Hello",\n    "What\'s up?", "***** GAME OVER *****", "".\n    '

    @typechecked
    def __init__(self, value):
        """Initialize self.  See help(type(self)) for accurate signature."""
        super().__init__(value)


class UnaryOp(Expression):
    __doc__ = 'Unary operator.'

    @typechecked
    def __init__(self, op, right):
        """Initialize self.  See help(type(self)) for accurate signature."""
        super().__init__('{op}{right}', op=op, right=right)


class BinaryOp(Expression):
    __doc__ = 'Binary operator.'

    @typechecked
    def __init__(self, op, left, right):
        """Initialize self.  See help(type(self)) for accurate signature."""
        super().__init__('({left} {op} {right})', op=op, left=left, right=right)


class ProcedureCall(Statement):
    __doc__ = 'Procedure call.'

    @typechecked
    def __init__(self, procedure, args):
        """Initialize self.  See help(type(self)) for accurate signature."""
        args_str = ', '.join(str(arg) for arg in args)
        super().__init__('{procedure} {args_str}', procedure=procedure, args=args,
          args_str=args_str)


class Body(Statement):
    __doc__ = 'Code block.\n\n    For example, global body or function body.\n    '

    @typechecked
    def __init__(self, statements):
        """Initialize self.  See help(type(self)) for accurate signature."""
        super().__init__('Code block', statements=statements)

    def __str__(self) -> str:
        """Implement str(self)."""
        result = '\n'.join(map(str, self['statements']))
        indented = indent(result, ' ' * IDENT)
        return indented


class Program(Body):
    __doc__ = 'Code block without identation.'

    def __str__(self) -> str:
        """Implement str(self)."""
        return '\n'.join(map(str, self['statements']))