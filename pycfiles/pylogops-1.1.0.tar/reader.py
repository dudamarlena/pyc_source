# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pylogo/reader.py
# Compiled at: 2007-10-14 14:35:27
__doc__ = '\nreader for pylogo\n  Ian Bicking <ianb@colorstudy.com>\n\nTokenizer/lexer.  Examples:\n\n    >>> tokenize(\'1 2 3\')\n    [1, 2, 3, \'\\n\']\n    >>> tokenize(\'fd 100\')\n    [\'fd\', 100, \'\\n\']\n    >>> tokenize(\'pr "hello\\nfd 100\\n\')\n    [\'pr\', \'"\', \'hello\', \'\\n\', \'fd\', 100, \'\\n\']\n    >>> tokenize(\'while [:a>2] [make :a :a+1]\')\n    [\'while\', \'[\', \':\', \'a\', \'>\', 2, \']\', \'[\', \'make\', \':\', \'a\', \':\', \'a\', \'+\', 1, \']\', \'\\n\']\n    >>> tokenize(\'>>>= <= <><> == =>=<\')\n    [\'>\', \'>\', \'>=\', \'<=\', \'<>\', \'<>\', \'=\', \'=\', \'=>\', \'=<\', \'\\n\']\n    >>> tokenize(\'apple? !apple .apple apple._me apple10 10apple\')\n    [\'apple?\', \'!apple\', \'.apple\', \'apple._me\', \'apple10\', 10, \'apple\', \'\\n\']\n\nNote that every file fed in is expected to end with a \'\\n\' (even if\nthe file doesn\'t actually).  We get common.EOF from the tokenizer when\nit is done.\n'
from __future__ import generators
import re, sys
from pylogo.common import *
import readline
word_matcher = '[a-zA-Z\\._\\?!][a-zA-Z0-9\\._\\?!]*'
word_re = re.compile(word_matcher)
only_word_re = re.compile('^%s$' % word_matcher)
number_re = re.compile('(?:[0-9][.0-9]*|-[0-9][0-9]*)')
symbols = '()[]+-/*":=><;'
extended_symbols = ['>=', '=>', '<=', '=<', '<>']
white_re = re.compile('[ \\t\\n\\r]+')

class FileTokenizer:
    """
    An interator over the tokens of a file.  Will prompt interactively
    if `prompt` is given.
    """
    __module__ = __name__

    def __init__(self, f, output=None, prompt=None):
        if type(f) is file:
            f = TrackingStream(f)
        self.file = f
        self.generator = self._generator()
        self.peeked = []
        self.prompt = prompt
        self.output = output
        self.context = []

    def __repr__(self):
        try:
            return '<FileTokenizer %x parsing %s:%i:%i>' % (id(self), self.file.name, self.file.row, self.file.col)
        except:
            return '<FileTokenizer %x parsing %r>' % (id(self), self.file)

    def print_prompt(self):
        if not self.prompt or not self.output:
            return
        if isinstance(self.prompt, str):
            prompt = self.prompt
        else:
            if self.context:
                context = self.context[(-1)]
            else:
                context = None
            prompt = self.prompt.get(context, '?')
        if prompt:
            self.output.write(prompt)
            self.output.flush()
        return

    def push_context(self, context):
        self.context.append(context)

    def pop_context(self):
        self.context.pop()

    def next(self):
        try:
            return self.generator.next()
        except StopIteration:
            import traceback
            traceback.print_exc()
            import sys
            sys.exit()

    def peek(self):
        if self.peeked:
            return self.peeked[0]
        p = self.next()
        self.peeked = [p]
        return p

    def _generator(self):
        """
        Generator - gets one token from the TrackingStream
        """
        while 1:
            if self.peeked:
                v = self.peeked[0]
                del self.peeked[0]
                yield v
            self.print_prompt()
            l = self.file.readline()
            while 1:
                if self.peeked:
                    v = self.peeked[0]
                    del self.peeked[0]
                    yield v
                m = white_re.match(l, pos=self.file.col)
                if m:
                    self.file.col = m.end()
                if l == '':
                    yield EOF
                    break
                if len(l) <= self.file.col:
                    yield '\n'
                    break
                c = l[self.file.col]
                try:
                    cnext = l[(self.file.col + 1)]
                except IndexError:
                    cnext = None

                if number_re.match(c) or c == '-' and cnext and number_re.match(cnext):
                    m = number_re.match(l, pos=self.file.col)
                    assert m
                    self.file.col = m.end()
                    n = m.group(0)
                    try:
                        yield int(n)
                    except ValueError:
                        try:
                            yield float(n)
                        except ValueError:
                            raise LogoSyntaxError(self.file, 'Not a number: %s' % repr(n))

                    else:
                        continue
                if c in symbols:
                    if cnext and c + cnext in extended_symbols:
                        self.file.col += 2
                        yield c + cnext
                    else:
                        self.file.col += 1
                        yield c
                elif word_re.match(c):
                    m = word_re.match(l, pos=self.file.col)
                    assert m
                    self.file.col = m.end()
                    yield m.group(0)
                else:
                    self.file.col += 1
                    yield c

        return


def is_word(tok):
    if isinstance(tok, str):
        return bool(only_word_re.search(tok))
    else:
        return False


class ListTokenizer:
    """
    This is just a cache of previously tokenized expressions.  So that
    [a block] can be treated like a stream of tokens.  The tokens are
    taken from `l`.
    """
    __module__ = __name__

    def __init__(self, l):
        self.list = l
        try:
            self.file = l.file
        except AttributeError:
            self.file = None

        self.pos = 0
        self.peeked = []
        return

    def __repr__(self):
        try:
            return '<ListTokenizer %x tokenizing list len=%i, pos=%i>' % (id(self), len(self.list), self.pos)
        except:
            return '<ListTokenizer %x>' % id(self)

    def push_context(self, context):
        pass

    def pop_context(self):
        pass

    def peek(self):
        if self.peeked:
            return self.peeked[0]
        p = self.next()
        self.peeked = [p]
        return p

    def next(self):
        if self.peeked:
            v = self.peeked[0]
            del self.peeked[0]
            return v
        if self.pos >= len(self.list):
            return EOF
        self.pos += 1
        return self.list[(self.pos - 1)]


class TrackingStream:
    """
    A file-like object that also keeps track of rows and columns,
    for tracebacks.
    """
    __module__ = __name__

    def __init__(self, file, name=None):
        self.file = file
        self.col = 0
        self.row = 0
        self.savedLines = []
        self.maxSavedLines = 10
        if name is None:
            self.name = self.file.name
        else:
            self.name = name
        return

    def readline(self):
        self.row += 1
        self.col = 0
        if self.file is sys.stdin:
            try:
                l = raw_input() + '\n'
            except EOFError:
                l = ''

        else:
            l = self.file.readline()
        self.savedLines.insert(0, l)
        if len(self.savedLines) > self.maxSavedLines:
            del self.savedLines[self.maxSavedLines:]
        return l

    def row_line(self, row):
        if row < self.row - len(self.savedLines):
            return
        return self.savedLines[(self.row - row)]

    def __repr__(self):
        s = repr(self.file)[:-1]
        return '%s %s:%s>' % (s, self.row, self.col)


def tokenize(s):
    from StringIO import StringIO
    input = StringIO(s)
    input.name = '<string>'
    tok = FileTokenizer(TrackingStream(input))
    result = []
    while 1:
        t = tok.next()
        if t is EOF:
            break
        result.append(t)

    return result


def main():
    import sys
    tok = FileTokenizer(TrackingStream(sys.stdin))
    while 1:
        print '>> %s' % repr(tok.next())


if __name__ == '__main__':
    main()