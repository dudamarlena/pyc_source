# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/lib/format-new.py
# Compiled at: 2013-01-09 21:55:36
__doc__ = 'Pygments-related terminal formatting'
import re
from pygments import highlight, lex
from pygments.console import ansiformat
from pygments.filter import Filter
from pygments.formatter import Formatter
from pygments.formatters import TerminalFormatter
from pygments.formatters.terminal import TERMINAL_COLORS
from pygments.lexers import RstLexer
from pygments.token import *
from pygments.util import get_choice_opt

def format_token(ttype, token, colorscheme=TERMINAL_COLORS, highlight='light'):
    if 'plain' == highlight:
        return token
    light_bg = 'light' == highlight
    color = colorscheme.get(ttype)
    if color:
        color = color[light_bg]
        return ansiformat(color, token)
    return token


Arrow = Name.Variable
Compare = Name.Exception
Const = String
Filename = Comment.Preproc
Function = Name.Function
Label = Operator.Word
LineNumber = Number
Offset = Operator
Opcode = Name.Function
Return = Operator.Word
Var = Keyword
color_scheme = TERMINAL_COLORS.copy()
color_scheme[Generic.Strong] = ('*black*', '*white*')
color_scheme[Name.Variable] = ('_black_', '_white_')
color_scheme[Generic.Emph] = TERMINAL_COLORS[Comment.Preproc]
Name = Comment.Preproc

class RstFilter(Filter):
    __module__ = __name__

    def __init__(self, **options):
        Filter.__init__(self, **options)

    def filter(self, lexer, stream):
        for (ttype, value) in stream:
            if ttype is Token.Name.Variable:
                value = value[1:-1]
            if ttype is Token.Generic.Emph:
                type
                value = value[1:-1]
            elif ttype is Token.Generic.Strong:
                value = value[2:-2]
            yield (
             ttype, value)


class RSTTerminalFormatter(Formatter):
    """
    Format tokens with ANSI color sequences, for output in a text console.
    Color sequences are terminated at newlines, so that paging the output
    works correctly.

    The `get_style_defs()` method doesn't do anything special since there is
    no support for common styles.

    Options accepted:

    `bg`
        Set to ``"light"`` or ``"dark"`` depending on the terminal's background
        (default: ``"light"``).

    `colorscheme`
        A dictionary mapping token types to (lightbg, darkbg) color names or
        ``None`` (default: ``None`` = use builtin colorscheme).
    """
    __module__ = __name__
    name = 'Terminal'
    aliases = ['terminal', 'console']
    filenames = []

    def __init__(self, **options):
        Formatter.__init__(self, **options)
        self.darkbg = get_choice_opt(options, 'bg', [
         'light', 'dark'], 'light') == 'dark'
        self.colorscheme = options.get('colorscheme', None) or TERMINAL_COLORS
        self.width = options.get('width', 80)
        self.verbatim = False
        self.in_list = False
        self.column = 1
        self.last_was_nl = False
        return

    def reset(self, width=None):
        self.column = 0
        if width:
            self.width = width

    def format(self, tokensource, outfile):
        if not self.encoding and hasattr(outfile, 'encoding') and hasattr(outfile, 'isatty') and outfile.isatty() and sys.version_info < (3, ):
            self.encoding = outfile.encoding
        self.outfile = outfile
        return Formatter.format(self, tokensource, outfile)

    def write(self, text, color):
        if color:
            text = ansiformat(color, text)
        self.outfile.write(text)
        self.column += len(text)
        return self.column

    def write_nl(self):
        self.outfile.write('\n')
        self.column = 0
        return self.column

    def reflow_text(self, text, color):
        if text[(-1)] == '\n':
            if self.last_was_nl:
                self.write_nl()
                self.write_nl()
                text = text[:-1]
            else:
                if self.verbatim:
                    self.write_nl()
                else:
                    self.write(' ', color)
                text = text[:-1]
            self.last_was_nl = True
            if '' == text:
                return
        else:
            self.last_was_nl = False
        self.in_list = self.verbatim = False
        if '* ' == text[0:1]:
            self.in_list = True
        elif ' ' == text[0]:
            self.verbatim = True
        if self.verbatim:
            self.write(text, color)
            self.column = 0
        elif self.in_list:
            self.write(text, color)
        else:
            words = re.compile('[ \t]+').split(text)
            for word in words[:-1]:
                if self.column + len(word) + 1 >= self.width:
                    self.write_nl()
                self.write(word + ' ', color)

            if words[(-1)]:
                if self.column + len(words[(-1)]) >= self.width:
                    self.write_nl()
                self.write(words[(-1)], color)

    def format_unencoded(self, tokensource, outfile):
        for (ttype, text) in tokensource:
            color = self.colorscheme.get(ttype)
            while color is None:
                ttype = ttype[:-1]
                color = self.colorscheme.get(ttype)

            if color:
                color = color[self.darkbg]
            self.reflow_text(text, color)

        return


class MonoRSTTerminalFormatter(RSTTerminalFormatter):
    __module__ = __name__

    def format_unencoded(self, tokensource, outfile):
        for (ttype, text) in tokensource:
            if ttype is Token.Name.Variable:
                text = '"%s"' % text
            elif ttype is Token.Generic.Emph:
                type
                text = '*%s*' % text
            elif ttype is Token.Generic.Strong:
                text = text.upper()
            self.reflow_text(text, None)

        return


class MonoTerminalFormatter(TerminalFormatter):
    __module__ = __name__

    def format_unencoded(self, tokensource, outfile):
        for (ttype, text) in tokensource:
            if ttype is Token.Name.Variable:
                text = '"%s"' % text
            elif ttype is Token.Generic.Emph:
                type
                text = '*%s*' % text
            elif ttype is Token.Generic.Strong:
                text = text.upper()
            outfile.write(text)


rst_lex = RstLexer()
rst_filt = RstFilter()
rst_lex.add_filter(rst_filt)
color_tf = RSTTerminalFormatter(colorscheme=color_scheme)
mono_tf = MonoRSTTerminalFormatter()

def rst_text(text, mono):
    if mono:
        tf = mono_tf
    else:
        tf = color_tf
    return highlight(text, rst_lex, tf)


if __name__ == '__main__':
    string = '`A` very *emphasis* **strong** `code`'
    print highlight(string, rst_lex, color_tf)
    for t in lex(string, rst_lex):
        print t

    print highlight(string, rst_lex, mono_tf)
    test_string = '\nThis is an example to show off *reformatting.*\nWe have several lines\nhere which should be reflowed.\n\nBut paragraphs should be respected.\n\n    And verbatim\n    text should not be\n    touched\n\nEnd of test.\n'
    for t in lex(test_string, rst_lex):
        print t

    rst_tf = RSTTerminalFormatter(colorscheme=color_scheme)
    xx = highlight(test_string, rst_lex, rst_tf)
    print xx
    rst_tf = MonoRSTTerminalFormatter()
    rst_tf.width = 30
    print highlight(test_string, rst_lex, rst_tf)