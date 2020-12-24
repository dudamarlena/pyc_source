# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/token.py
# Compiled at: 2019-08-15 23:53:38
# Size of source mod 2**32: 1421 bytes
__doc__ = '\nThe Token class, interchangeable with ``pygments.token``.\n\nA `Token` has some semantics for a piece of text that is given a style through\na :class:`~prompt_tool_kit.styles.Style` class. A pygments lexer for instance,\nreturns a list of (Token, text) tuples. Each fragment of text has a token\nassigned, which when combined with a style sheet, will determine the fine\nstyle.\n'
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