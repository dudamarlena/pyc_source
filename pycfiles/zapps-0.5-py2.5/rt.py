# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/zapps/rt.py
# Compiled at: 2008-04-06 20:45:05
from string import join, count, find, rfind
import re, struct

class SyntaxError(Exception):
    """When we run into an unexpected token, this is the exception to use"""

    def __init__(self, pos=-1, msg='Bad Token'):
        Exception.__init__(self)
        self.pos = pos
        self.msg = msg

    def __repr__(self):
        if self.pos < 0:
            return '#<syntax-error>'
        else:
            return 'SyntaxError[@ char %s: %s]' % (repr(self.pos), self.msg)


class NoMoreTokens(Exception):
    """Another exception object, for when we run out of tokens"""
    pass


class Scanner:

    def __init__(self, patterns, ignore, input):
        """Patterns is [(terminal,regex)...]
        Ignore is [terminal,...];
        Input is a string"""
        self.tokens = []
        self.restrictions = []
        self.input = input
        self.pos = 0
        self.ignore = ignore
        if patterns is not None:
            self.patterns = []
            for (k, r) in patterns:
                self.patterns.append((k, re.compile(r)))

        return

    def token(self, i, restrict=0):
        """Get the i'th token, and if i is one past the end, then scan
        for another token; restrict is a list of tokens that
        are allowed, or 0 for any token."""
        if i == len(self.tokens):
            self.scan(restrict)
        if i < len(self.tokens):
            if restrict and self.restrictions[i]:
                for r in restrict:
                    if r not in self.restrictions[i]:
                        raise NotImplementedError('Unimplemented: restriction set changed')

            return self.tokens[i]
        raise NoMoreTokens()

    def __repr__(self):
        """Print the last 10 tokens that have been scanned in"""
        output = ''
        for t in self.tokens[-10:]:
            output = '%s\n  (@%s)  %s  =  %s' % (output, t[0], t[2], repr(t[3]))

        return output

    def skip(self, length):
        """Skips without returning the length number of chars in the input."""
        self.pos += length

    def eat(self, length):
        """Returns a chunk from the current pos of given length and then
        advances the pos to the next char after that."""
        chunk = self.input[self.pos:self.pos + length]
        self.skip(length)
        return chunk

    def scan(self, restrict):
        """Should scan another token and add it to the list, self.tokens,
        and add the restriction to self.restrictions"""
        while 1:
            best_match = -1
            best_pat = '(error)'
            for (p, regexp) in self.patterns:
                if restrict and p not in restrict and p not in self.ignore:
                    continue
                m = regexp.match(self.input, self.pos)
                if m and len(m.group(0)) > best_match:
                    best_pat = p
                    best_match = len(m.group(0))

            if best_pat == '(error)' and best_match < 0:
                msg = 'Bad Token'
                if restrict:
                    msg = 'Trying to find one of ' + join(restrict, ', ')
                raise SyntaxError(self.pos, msg)
            if best_pat not in self.ignore:
                token = (self.pos, self.pos + best_match, best_pat, self.eat(best_match))
                if not self.tokens or token != self.tokens[(-1)]:
                    self.tokens.append(token)
                    self.restrictions.append(restrict)
                return
            else:
                self.skip(best_match)


class Parser:

    def __init__(self, scanner):
        self._scanner = scanner
        self._pos = 0

    def _peek(self, *types):
        """Returns the token type for lookahead; if there are any args
        then the list of args is the set of token types to allow"""
        tok = self._scanner.token(self._pos, types)
        return tok[2]

    def _eat(self, length):
        """Returns the given amount of the internal buffer then
        increments by that much to continue parsing."""
        return self._scanner.eat(length)

    def _scan(self, type):
        """Returns the matched text, and moves to the next token"""
        tok = self._scanner.token(self._pos, [type])
        if tok[2] != type:
            raise SyntaxError(tok[0], 'Trying to find ' + type)
        self._pos = 1 + self._pos
        return tok[3]

    def _unpack(self, expr):
        """Performs a python unpack on the current input
        and returns that tuple."""
        piece = self._eat(struct.calcsize(expr))
        return struct.unpack(expr, piece)


def print_error(input, err, scanner):
    """This is a really dumb long function to print error messages nicely."""
    p = err.pos
    line = count(input[:p], '\n')
    print err.msg + ' on line ' + repr(line + 1) + ':'
    text = input[max(p - 80, 0):p + 80]
    p = p - max(p - 80, 0)
    i = rfind(text[:p], '\n')
    j = rfind(text[:p], '\r')
    if i < 0 or 0 <= j < i:
        i = j
    if 0 <= i < p:
        p = p - i - 1
        text = text[i + 1:]
    i = find(text, '\n', p)
    j = find(text, '\r', p)
    if i < 0 or 0 <= j < i:
        i = j
    if i >= 0:
        text = text[:i]
    while len(text) > 70 and p > 60:
        text = '...' + text[10:]
        p = p - 7

    print '> ', text
    print '> ', ' ' * p + '^'
    print 'List of nearby tokens:', scanner


def wrap_error_reporter(parser, rule):
    return_value = None
    try:
        return_value = getattr(parser, rule)()
    except SyntaxError, s:
        input = parser._scanner.input
        try:
            print_error(input, s, parser._scanner)
        except ImportError:
            print 'Syntax Error', s.msg, 'on line', 1 + count(input[:s.pos], '\n')

    except NoMoreTokens:
        print 'Could not complete parsing; stopped around here:'
        print parser._scanner

    return return_value