# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/token.py
# Compiled at: 2019-08-15 23:53:38
# Size of source mod 2**32: 1421 bytes
"""
The Token class, interchangeable with ``pygments.token``.

A `Token` has some semantics for a piece of text that is given a style through
a :class:`~prompt_tool_kit.styles.Style` class. A pygments lexer for instance,
returns a list of (Token, text) tuples. Each fragment of text has a token
assigned, which when combined with a style sheet, will determine the fine
style.
"""
__all__ = ('Token', 'ZeroWidthEscape')

class _TokenType(tuple):

    def __getattr__(self, val):
        if not val or not val[0].isupper():
            return tuple.__getattribute__(self, val)
        else:
            new = _TokenType(self + (val,))
            setattr(self, val, new)
            return new

    def __repr__(self):
        return 'Token' + (self and '.' or '') + '.'.join(self)


try:
    from pygments.token import Token
except ImportError:
    Token = _TokenType()

ZeroWidthEscape = Token.ZeroWidthEscape