# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/lib/format.py
# Compiled at: 2019-10-10 07:55:25
"""Pygments-related terminal formatting"""
import re, sys, pyficache
from pygments import highlight, lex
from pygments.console import ansiformat
from pygments.filter import Filter
from pygments.formatter import Formatter
from pygments.formatters import TerminalFormatter
from pygments.formatters.terminal import TERMINAL_COLORS
from pygments.lexers import RstLexer
from pygments.token import Comment, Generic, Keyword, Name, Number, Operator, String, Token
from pygments.util import get_choice_opt
color_scheme = TERMINAL_COLORS.copy()
color_scheme[Generic.Strong] = ('*black*', '*white*')
color_scheme[Name.Variable] = ('_black_', '_white_')
color_scheme[Generic.Strong] = ('*black*', '*white*')
color_scheme[Name.Variable] = ('_black_', '_white_')
color_scheme[Generic.Emph] = color_scheme[Comment.Preproc]
pyficache.dark_terminal_formatter.colorscheme = color_scheme
pyficache.light_terminal_formatter.colorscheme = color_scheme

def format_token(ttype, token, colorscheme=color_scheme, highlight='light'):
    if 'plain' == highlight:
        return token
    dark_bg = 'dark' == highlight
    color = colorscheme.get(ttype)
    if color:
        color = color[dark_bg]
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
Verbatim = String
Name = Comment.Preproc

class RstFilter(Filter):

    def __init__(self, **options):
        Filter.__init__(self, **options)

    def filter(self, lexer, stream):
        last_was_heading_title = ''
        for ttype, value in stream:
            if ttype is Token.Name.Variable:
                value = value[1:-1]
                last_was_heading_title = ''
            if ttype is Token.Generic.Emph:
                value = value[1:-1]
                last_was_heading_title = ''
            else:
                if ttype is Token.Generic.Strong:
                    value = value[2:-2]
                    last_was_heading_title = ''
                else:
                    if ttype is Token.Text and last_was_heading_title and value == '\n':
                        value = ''
                    elif ttype is Token.Generic.Heading:
                        if last_was_heading_title and re.match('^(?:[=]|[-])+$', value):
                            value = ''
                            last_was_heading_title = ''
                        else:
                            last_was_heading_title = value
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
    name = 'Terminal'
    aliases = ['terminal', 'console']
    filenames = []

    def __init__(self, **options):
        Formatter.__init__(self, **options)
        self.darkbg = get_choice_opt(options, 'bg', [
         'light', 'dark'], 'light') != 'dark'
        self.colorscheme = options.get('colorscheme', None) or color_scheme
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

    def write_verbatim(self, text):
        if self.__class__ != MonoRSTTerminalFormatter:
            cs = self.colorscheme.get(Verbatim)
            color = cs[self.darkbg]
        else:
            color = None
        return self.write(text, color)

    def write(self, text, color):
        color_text = text
        if color:
            color_text = ansiformat(color, color_text)
        self.outfile.write(color_text)
        self.column += len(text)
        return self.column

    def write_nl(self):
        self.outfile.write('\n')
        self.column = 0
        return self.column

    def reflow_text(self, text, ttype, color):
        if text == '::' and ttype == Token.Literal.String.Escape:
            self.verbatim = 'colon-verbatim'
            return
        if self.verbatim == 'colon-verbatim' and ttype == Token.Text and text == '\n\n':
            self.write_nl()
            self.last_was_nl = True
            return
        if self.verbatim == 'colon-verbatim' and ttype == Token.Text and text == '\n':
            self.write_nl()
            self.last_was_nl = False
            return
        last_last_nl = self.last_was_nl
        if text == '':
            pass
        else:
            if text[(-1)] == '\n':
                if self.last_was_nl:
                    self.write_nl()
                    self.write_nl()
                    text = text[:-1]
                else:
                    if self.verbatim:
                        self.write_verbatim(text)
                        self.column = 0
                        self.verbatim = len(text) >= 2 and text[(-2)] == '\n'
                        self.last_was_nl = True
                        return
                    self.write(' ', color)
                    text = text[:-1]
                self.last_was_nl = True
                if '' == text:
                    return
                while text[(-1)] == '\n':
                    self.write_nl()
                    text = text[:-1]
                    if '' == text:
                        return

            else:
                self.last_was_nl = False
            self.in_list = False
            if last_last_nl:
                if ' * ' == text[0:3]:
                    self.in_list = True
                elif '  ' == text[0:2]:
                    self.verbatim = self.verbatim or True
            if self.verbatim:
                self.write_verbatim(text)
            else:
                if self.in_list:
                    self.write(text, color)
                else:
                    words = re.compile('[ \t]+').split(text)
                    for word in words[:-1]:
                        if self.column + len(word) + 1 >= self.width:
                            self.write_nl()
                        if not (self.column == 0 and word == ''):
                            self.write(word + ' ', color)
                            continue

        if words[(-1)]:
            if self.column + len(words[(-1)]) >= self.width:
                self.write_nl()
            self.write(words[(-1)], color)

    def format_unencoded(self, tokensource, outfile):
        for ttype, text in tokensource:
            color = self.colorscheme.get(ttype)
            resolved_type = ttype
            while color is None:
                resolved_type = resolved_type[:-1]
                color = self.colorscheme.get(resolved_type)

            if color:
                color = color[self.darkbg]
            self.reflow_text(text, ttype, color)

        return


class MonoRSTTerminalFormatter(RSTTerminalFormatter):

    def format_unencoded(self, tokensource, outfile):
        for ttype, text in tokensource:
            if ttype is Token.Name.Variable:
                text = '"%s"' % text
            else:
                if ttype is Token.Generic.Emph:
                    text = '*%s*' % text
                elif ttype is Token.Generic.Strong:
                    text = text.upper()
            self.reflow_text(text, ttype, None)

        return


class MonoTerminalFormatter(TerminalFormatter):

    def format_unencoded(self, tokensource, outfile):
        for ttype, text in tokensource:
            if ttype is Token.Name.Variable:
                text = '"%s"' % text
            else:
                if ttype is Token.Generic.Emph:
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

def rst_text(text, mono, width=80):
    if mono:
        tf = mono_tf
    else:
        tf = color_tf
    tf.reset(width)
    return highlight(text, rst_lex, tf)


if __name__ == '__main__':

    def show_it(string, tf, width=80):
        tf.reset(width)
        print('=' * 30)
        for t in lex(string, rst_lex):
            print(t)

        print('-' * 30)
        print(highlight(string, rst_lex, tf))


    test_string = '\nHeading\n-------\n\nThis is an example to show off *reformatting.*\nWe have several lines\nhere which should be reflowed.\n\nBut paragraphs should be respected.\n\n   And verbatim\n   text should not be\n   touched\n\nEnd of test.\n'
    rst_tf = MonoRSTTerminalFormatter()
    show_it(test_string, rst_tf, 30)
    text = '**break** [*location*] [if *condition*]]\n\nWith a line number argument, set a break there in the current file.\nWith a function name, set a break at first executable line of that\nfunction.  Without argument, set a breakpoint at current location.  If\na second argument is `if`, subsequent arguments given an expression\nwhich must evaluate to true before the breakpoint is honored.\n\nThe location line number may be prefixed with a filename or module\nname and a colon. Files is searched for using *sys.path*, and the `.py`\nsuffix may be omitted in the file name.\n\nExamples:\n---------\n\n   break              # Break where we are current stopped at\n   break if i < j     # Break at current line if i < j\n   break 10           # Break on line 10 of the file we are\n                      #  currently stopped at\n   break os.path.join # Break in function os.path.join\n   break os.path:45   # Break on line 45 of os.path\n   break myfile:5 if i < j # Same as above but only if i < j\n   break myfile.py:45 # Break on line 45 of myfile.py\n   break myfile:45    # Same as above.\n'
    show_it(text, rst_tf)
    rst_tf = RSTTerminalFormatter(colorscheme=color_scheme)
    show_it(text, rst_tf)
    text = 'Examples:\n---------\n::\n\n    disasm\n    disasm *10, *20\n    '
    show_it(text, rst_tf)