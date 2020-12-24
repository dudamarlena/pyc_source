# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.9.1-i386/egg/ZestyParser/Helpers.py
# Compiled at: 2007-04-30 17:11:17
"""
@version: 0.8.1
@author: Adam Atlas
@copyright: Copyright 2006-2007 Adam Atlas. Released under the MIT license (see LICENSE.txt).
@contact: adam@atlas.st
"""
from Tokens import *
import re, Tokens, Parser
__all__ = [
 '_next_', '_this_', '_top_', '_sp_', 'UNARY', 'BINARY', 'LEFT', 'CENTER', 'RIGHT', 'oper', 'Float', 'Int', 'ExpressionHelper', 'QuoteHelper', 'EscapeHelper', 'FromOct', 'FromHex', 'PyEsc', 'SameChar', 'EscCh', 'IndentHelper', 'EncloseHelper']
_ = Placeholder()
_next_ = _('next')
_this_ = _('this')
_top_ = _('top')
_sp_ = _('sp')
UNARY = 1
BINARY = 2
LEFT = -1
CENTER = 0
RIGHT = 1

def _funcmap(f):

    def newfunc(arg):
        return f(*arg)

    return newfunc


class Oper(TokenSequence):
    __module__ = __name__


def oper(symbol, operation=None, ops=BINARY, pos=CENTER):
    if isinstance(symbol, basestring):
        symtok = Omit(Raw(symbol))
    else:
        symtok = symbol
    if ops == BINARY:
        if pos == LEFT:
            tok = Oper([symtok, _next_, _this_])
        elif pos == CENTER:
            tok = Oper([_next_, symtok, _this_])
        elif pos == RIGHT:
            tok = Oper([_next_, _this_, symtok])
    elif ops == UNARY:
        if pos in (LEFT, CENTER):
            tok = Oper([symtok, _next_])
        elif pos == RIGHT:
            tok = Oper([_next_, symtok])
    tok = Tokens._pad(_sp_, tok)
    if operation:
        tok.callback = _funcmap(operation)
    tok.name = '<Oper %s>' % symbol
    return tok


Float = RE('[0-9]*\\.[0-9]+', group=0, to=float)
Int = RE('[0-9]+', group=0, to=int)

def ExpressionHelper(toks, space=Whitespace):
    toks = [toks[0]] + [ t | _next_ for t in toks ]
    for i in range(1, len(toks)):
        toks[i] %= dict(next=toks[(i - 1)], this=toks[i], top=toks[(-1)])

    if space:
        for (i, tok) in enumerate(toks):
            if not isinstance(tok, Oper):
                toks[i] = Tokens._pad(_sp_, tok)

    toks[(-1)] %= {_sp_: space}
    return toks[(-1)]


def QuoteHelper(esc='\\', quotes=('"', "'"), allowed='.', *a, **k):
    r = []
    for q in quotes:
        if len(q) == 2:
            (left, right) = (
             q[0], q[1])
        else:
            left = right = q[0]
        if isinstance(left, basestring):
            left = Raw(left)
        if isinstance(right, basestring):
            right = Raw(right) ^ True
        o = left + Only(RE('(?:%s%s|[^%s])*' % (re.escape(esc), allowed, re.escape(right.desc)), group=0)) + right
        r.append(o)

    default_callback = EscapeHelper((EscCh(symbol=esc, anything=True), SameChar))
    return CompositeToken(r, callback=default_callback, *a, **k)


class EscapeHelper:
    __module__ = __name__

    def __init__(self, *escapes):
        self.escapes = [ (re.compile(t[0]), t[1]) for t in escapes ]

    def __call__(self, val):
        if hasattr(val, 'group'):
            val = val.group(0)
        for (regex, replace) in self.escapes:
            val = regex.sub(replace, val)

        return val


def FromOct(m):
    return chr(int(m.group(1), 8))


def FromHex(m):
    return chr(int(m.group(1), 16))


def PyEsc(m):
    return eval('"\\%s"' % m.group(1))


def SameChar(m):
    return m.group(1)


def EscCh(chars='', symbol='\\', anything=False):
    symbol = re.escape(symbol)
    chars = [ re.escape(c) for c in chars ]
    return (anything and '%s(.)' or '%%s(%s)' % ('|').join(chars)) % symbol


class IndentationLevel(AbstractToken):
    __module__ = __name__

    def __init__(self, depth, space, tabwidth=8, *a, **k):
        AbstractToken.__init__(self, depth, *a, **k)
        self.space = space
        self.tabwidth = 8

    def __call__(self, parser, origCursor):
        if not parser.skip(self.space):
            raise NotMatched
        i = parser.data.rfind('\n', 0, parser.cursor) + 1
        level = len(parser.data[i:parser.cursor].expandtabs(self.tabwidth))
        if level < self.desc:
            raise Parser.NotMatched
        elif level > self.desc:
            parser.cursor = origCursor + self.desc
        return True


class IndentHelper(Tokens.SingleReplacing, AbstractToken):
    __module__ = __name__

    def __init__(self, desc, space='[ \t]*', tabwidth=8, skip=None, *a, **k):
        AbstractToken.__init__(self, desc, *a, **k)
        if isinstance(space, basestring):
            space = RE(space, group=0)
        self.space = space
        self.tabwidth = 8
        self.skip = skip
        self.key = id(IndentHelper)

    def __call__(self, parser, origCursor):
        prev_level = parser.context.setdefault(self.key, -1)
        parser.scan(self.space)
        last_nl = parser.data.rfind('\n', 0, parser.cursor) + 1
        new_level = len(parser.data[last_nl:parser.cursor].expandtabs(self.tabwidth))
        if prev_level >= new_level:
            raise Parser.NotMatched
        parser.context[self.key] = new_level
        parser.cursor = origCursor
        out = []
        t_line = IndentationLevel(new_level, self.space, self.tabwidth) + Only(self.desc)
        while 1:
            if self.skip:
                parser.skip(self.skip)
            line = parser.scan(t_line)
            if not parser.last:
                break
            out.append(line)

        if self.skip:
            parser.skip(self.skip)
        parser.context[self.key] = prev_level
        if not len(out):
            raise Parser.NotMatched
        return out


class EncloseHelper(Tokens.SingleReplacing, AbstractToken):
    __module__ = __name__

    def __init__(self, pairs, content, space=Whitespace, *a, **k):
        AbstractToken.__init__(self, content, *a, **k)
        self.ptoks = []
        self.space = space
        if not isinstance(pairs, list):
            pairs = [
             pairs]
        for (start, end) in pairs:
            if isinstance(start, basestring):
                start = Raw(start)
            if isinstance(end, basestring):
                end = Raw(end)
            self.ptoks.append((start, end ^ True))

    def __call__(self, parser, origCursor):
        for (start, end) in self.ptoks:
            if not parser.skip(start):
                continue
            if self.space is Whitespace:
                parser.skip(parser.whitespace)
            elif self.space:
                parser.skip(self.space)
            v = parser.scan(self.desc)
            if not parser.last:
                continue
            if self.space is Whitespace:
                parser.skip(parser.whitespace)
            elif self.space:
                parser.skip(self.space)
            parser.skip(end)
            return v

        raise Parser.NotMatched