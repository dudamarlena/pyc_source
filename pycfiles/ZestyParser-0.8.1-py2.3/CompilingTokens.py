# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.9.1-i386/egg/ZestyParser/CompilingTokens.py
# Compiled at: 2007-04-18 17:20:23
import re, copy
from Parser import NotMatched, ParseError
import Tokens
__all__ = (
 'CompilingToken', 'Token', 'RawToken', 'CompositeToken', 'TokenSequence', 'TakeToken', 'TokenSeries', 'EmptyToken', 'Default', 'Skip', 'Omit', 'Defer', 'EOF')
rstack = []

class CompilingBase:
    __module__ = __name__

    def __add__(self, other):
        return TokenSequence([self, other])

    def __or__(self, other):
        return CompositeToken([self, other])


class CompilingToken(CompilingBase, Tokens.AbstractToken):
    __module__ = __name__
    code = None

    def __init__(self, desc, code, callback=None, as=None, name=None):
        Tokens.AbstractToken.__init__(self, desc, callback, as, name)
        self.code = code

    def __call__(self, parser, origCursor):
        if type(self.code) is str:
            x = {}
            exec 'def f(self, parser, origCursor):\n' + self.code in globals(), x
            self.code = x['f']
        return self.preprocessResult(parser, self.code(self, parser, origCursor), origCursor)


class Token(CompilingBase, Tokens.Token):
    __module__ = __name__


class RawToken(CompilingToken, Tokens.RawToken):
    __module__ = __name__

    def __init__(self, string, callback=None, as=None, name=None, caseInsensitive=False):
        code = '\n end = origCursor + %i\n d = parser.data[origCursor:end]\n' % len(string)
        if caseInsensitive:
            string = string.lower()
            code += '\n if d.lower() == self.desc:\n'
        else:
            code += '\n if d == self.desc:\n'
        code += '\n  parser.cursor = end\n  return d\n else: raise NotMatched\n'
        CompilingToken.__init__(self, string, code, callback, as, name)


class CompositeToken(CompilingBase, Tokens.CompositeToken):
    __module__ = __name__


class TokenSequence(CompilingToken, Tokens.TokenSequence):
    __module__ = __name__

    def __init__(self, desc, callback=None, as=None, name=None):
        code = ' o = []; d = self.desc\n'
        for (i, t) in zip(range(len(desc)), desc):
            code += '\n r = parser.scan(d[%i])\n if parser.last is None: raise NotMatched\n' % i
            if not isinstance(t, (Skip, Omit)):
                code += '\n o.append(r)\n'

        code += ' return o'
        self.finalcode = code
        CompilingToken.__init__(self, desc, code, callback, as, name)

    def __add__(self, other):
        if isinstance(other, TokenSequence):
            return TokenSequence(self.desc + other.desc)
        elif hasattr(other, '__iter__'):
            return TokenSequence(self.desc + list(other))
        else:
            return TokenSequence(self.desc + [other])

    def __iadd__(self, other):
        if isinstance(other, TokenSequence):
            self.desc += other.desc
        elif hasattr(other, '__iter__'):
            self.desc += list(other)
        else:
            self.desc.append(other)
        return self


class TakeToken(CompilingBase, Tokens.TakeToken):
    __module__ = __name__


class TokenSeries(CompilingBase, Tokens.TokenSeries):
    __module__ = __name__


class Default(CompilingBase, Tokens.Default):
    __module__ = __name__


EmptyToken = Default('')

class Skip(CompilingBase, Tokens.Skip):
    __module__ = __name__


class Omit(CompilingBase, Tokens.Omit):
    __module__ = __name__


class Defer(CompilingBase, Tokens.Defer):
    __module__ = __name__


class _EOF(CompilingBase, Tokens._EOF):
    __module__ = __name__


EOF = _EOF(None)