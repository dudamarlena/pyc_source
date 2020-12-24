# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/utils/jslex.py
# Compiled at: 2019-02-14 00:35:17
"""JsLex: a lexer for Javascript"""
from __future__ import unicode_literals
import re

class Tok(object):
    """
    A specification for a token class.
    """
    num = 0

    def __init__(self, name, regex, next=None):
        self.id = Tok.num
        Tok.num += 1
        self.name = name
        self.regex = regex
        self.next = next


def literals(choices, prefix=b'', suffix=b''):
    """
    Create a regex from a space-separated list of literal `choices`.

    If provided, `prefix` and `suffix` will be attached to each choice
    individually.
    """
    return (b'|').join(prefix + re.escape(c) + suffix for c in choices.split())


class Lexer(object):
    """
    A generic multi-state regex-based lexer.
    """

    def __init__(self, states, first):
        self.regexes = {}
        self.toks = {}
        for state, rules in states.items():
            parts = []
            for tok in rules:
                groupid = b't%d' % tok.id
                self.toks[groupid] = tok
                parts.append(b'(?P<%s>%s)' % (groupid, tok.regex))

            self.regexes[state] = re.compile((b'|').join(parts), re.MULTILINE | re.VERBOSE)

        self.state = first

    def lex(self, text):
        """
        Lexically analyze `text`.

        Yields pairs (`name`, `tokentext`).
        """
        end = len(text)
        state = self.state
        regexes = self.regexes
        toks = self.toks
        start = 0
        while start < end:
            for match in regexes[state].finditer(text, start):
                name = match.lastgroup
                tok = toks[name]
                toktext = match.group(name)
                start += len(toktext)
                yield (tok.name, toktext)
                if tok.next:
                    state = tok.next
                    break

        self.state = state


class JsLexer(Lexer):
    """
    A Javascript lexer

    >>> lexer = JsLexer()
    >>> list(lexer.lex("a = 1"))
    [('id', 'a'), ('ws', ' '), ('punct', '='), ('ws', ' '), ('dnum', '1')]

    This doesn't properly handle non-ASCII characters in the Javascript source.
    """
    both_before = [
     Tok(b'comment', b'/\\*(.|\\n)*?\\*/'),
     Tok(b'linecomment', b'//.*?$'),
     Tok(b'ws', b'\\s+'),
     Tok(b'keyword', literals(b'\n                           break case catch class const continue debugger\n                           default delete do else enum export extends\n                           finally for function if import in instanceof\n                           new return super switch this throw try typeof\n                           var void while with\n                           ', suffix=b'\\b'), next=b'reg'),
     Tok(b'reserved', literals(b'null true false', suffix=b'\\b'), next=b'div'),
     Tok(b'id', b'\n                  ([a-zA-Z_$   ]|\\\\u[0-9a-fA-Z]{4})   # first char\n                  ([a-zA-Z_$0-9]|\\\\u[0-9a-fA-F]{4})*  # rest chars\n                  ', next=b'div'),
     Tok(b'hnum', b'0[xX][0-9a-fA-F]+', next=b'div'),
     Tok(b'onum', b'0[0-7]+'),
     Tok(b'dnum', b'\n                    (   (0|[1-9][0-9]*)     # DecimalIntegerLiteral\n                        \\.                  # dot\n                        [0-9]*              # DecimalDigits-opt\n                        ([eE][-+]?[0-9]+)?  # ExponentPart-opt\n                    |\n                        \\.                  # dot\n                        [0-9]+              # DecimalDigits\n                        ([eE][-+]?[0-9]+)?  # ExponentPart-opt\n                    |\n                        (0|[1-9][0-9]*)     # DecimalIntegerLiteral\n                        ([eE][-+]?[0-9]+)?  # ExponentPart-opt\n                    )\n                    ', next=b'div'),
     Tok(b'punct', literals(b'\n                         >>>= === !== >>> <<= >>= <= >= == != << >> &&\n                         || += -= *= %= &= |= ^=\n                         '), next=b'reg'),
     Tok(b'punct', literals(b'++ -- ) ]'), next=b'div'),
     Tok(b'punct', literals(b'{ } ( [ . ; , < > + - * % & | ^ ! ~ ? : ='), next=b'reg'),
     Tok(b'string', b'"([^"\\\\]|(\\\\(.|\\n)))*?"', next=b'div'),
     Tok(b'string', b"'([^'\\\\]|(\\\\(.|\\n)))*?'", next=b'div')]
    both_after = [
     Tok(b'other', b'.')]
    states = {b'div': both_before + [Tok(b'punct', literals(b'/= /'), next=b'reg')] + both_after, 
       b'reg': both_before + [Tok(b'regex', b'\n                    /                       # opening slash\n                    # First character is..\n                    (   [^*\\\\/[]            # anything but * \\ / or [\n                    |   \\\\.                 # or an escape sequence\n                    |   \\[                  # or a class, which has\n                            (   [^\\]\\\\]     #   anything but \\ or ]\n                            |   \\\\.         #   or an escape sequence\n                            )*              #   many times\n                        \\]\n                    )\n                    # Following characters are same, except for excluding a star\n                    (   [^\\\\/[]             # anything but \\ / or [\n                    |   \\\\.                 # or an escape sequence\n                    |   \\[                  # or a class, which has\n                            (   [^\\]\\\\]     #   anything but \\ or ]\n                            |   \\\\.         #   or an escape sequence\n                            )*              #   many times\n                        \\]\n                    )*                      # many times\n                    /                       # closing slash\n                    [a-zA-Z0-9]*            # trailing flags\n                ', next=b'div')] + both_after}

    def __init__(self):
        super(JsLexer, self).__init__(self.states, b'reg')


def prepare_js_for_gettext(js):
    """
    Convert the Javascript source `js` into something resembling C for
    xgettext.

    What actually happens is that all the regex literals are replaced with
    "REGEX".
    """

    def escape_quotes(m):
        """Used in a regex to properly escape double quotes."""
        s = m.group(0)
        if s == b'"':
            return b'\\"'
        else:
            return s

    lexer = JsLexer()
    c = []
    for name, tok in lexer.lex(js):
        if name == b'regex':
            tok = b'"REGEX"'
        elif name == b'string':
            if tok.startswith(b"'"):
                guts = re.sub(b'\\\\.|.', escape_quotes, tok[1:-1])
                tok = b'"' + guts + b'"'
        elif name == b'id':
            tok = tok.replace(b'\\', b'U')
        c.append(tok)

    return (b'').join(c)