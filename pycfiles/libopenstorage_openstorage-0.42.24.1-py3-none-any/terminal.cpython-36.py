# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/Pygments/pygments/formatters/terminal.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 4997 bytes
"""
    pygments.formatters.terminal
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Formatter for terminal output with ANSI sequences.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import sys
from pygments.formatter import Formatter
from pygments.token import Keyword, Name, Comment, String, Error, Number, Operator, Generic, Token, Whitespace
from pygments.console import ansiformat
from pygments.util import get_choice_opt
__all__ = [
 'TerminalFormatter']
TERMINAL_COLORS = {Token: ('', ''), 
 Whitespace: ('gray', 'brightblack'), 
 Comment: ('gray', 'brightblack'), 
 Comment.Preproc: ('cyan', 'brightcyan'), 
 Keyword: ('blue', 'brightblue'), 
 Keyword.Type: ('cyan', 'brightcyan'), 
 Operator.Word: ('magenta', 'brightmagenta'), 
 Name.Builtin: ('cyan', 'brightcyan'), 
 Name.Function: ('green', 'brightgreen'), 
 Name.Namespace: ('_cyan_', '_brightcyan_'), 
 Name.Class: ('_green_', '_brightgreen_'), 
 Name.Exception: ('cyan', 'brightcyan'), 
 Name.Decorator: ('brightblack', 'gray'), 
 Name.Variable: ('red', 'brightred'), 
 Name.Constant: ('red', 'brightred'), 
 Name.Attribute: ('cyan', 'brightcyan'), 
 Name.Tag: ('brightblue', 'brightblue'), 
 String: ('yellow', 'yellow'), 
 Number: ('blue', 'brightblue'), 
 Generic.Deleted: ('brightred', 'brightred'), 
 Generic.Inserted: ('green', 'brightgreen'), 
 Generic.Heading: ('**', '**'), 
 Generic.Subheading: ('*magenta*', '*brightmagenta*'), 
 Generic.Prompt: ('**', '**'), 
 Generic.Error: ('brightred', 'brightred'), 
 Error: ('_brightred_', '_brightred_')}

class TerminalFormatter(Formatter):
    __doc__ = '\n    Format tokens with ANSI color sequences, for output in a text console.\n    Color sequences are terminated at newlines, so that paging the output\n    works correctly.\n\n    The `get_style_defs()` method doesn\'t do anything special since there is\n    no support for common styles.\n\n    Options accepted:\n\n    `bg`\n        Set to ``"light"`` or ``"dark"`` depending on the terminal\'s background\n        (default: ``"light"``).\n\n    `colorscheme`\n        A dictionary mapping token types to (lightbg, darkbg) color names or\n        ``None`` (default: ``None`` = use builtin colorscheme).\n\n    `linenos`\n        Set to ``True`` to have line numbers on the terminal output as well\n        (default: ``False`` = no line numbers).\n    '
    name = 'Terminal'
    aliases = ['terminal', 'console']
    filenames = []

    def __init__(self, **options):
        (Formatter.__init__)(self, **options)
        self.darkbg = get_choice_opt(options, 'bg', [
         'light', 'dark'], 'light') == 'dark'
        self.colorscheme = options.get('colorscheme', None) or TERMINAL_COLORS
        self.linenos = options.get('linenos', False)
        self._lineno = 0

    def format(self, tokensource, outfile):
        if not self.encoding:
            if hasattr(outfile, 'encoding'):
                if hasattr(outfile, 'isatty'):
                    if outfile.isatty():
                        if sys.version_info < (3, ):
                            self.encoding = outfile.encoding
        return Formatter.format(self, tokensource, outfile)

    def _write_lineno(self, outfile):
        self._lineno += 1
        outfile.write('%s%04d: ' % (self._lineno != 1 and '\n' or '', self._lineno))

    def _get_color(self, ttype):
        colors = self.colorscheme.get(ttype)
        while colors is None:
            ttype = ttype.parent
            colors = self.colorscheme.get(ttype)

        return colors[self.darkbg]

    def format_unencoded(self, tokensource, outfile):
        if self.linenos:
            self._write_lineno(outfile)
        for ttype, value in tokensource:
            color = self._get_color(ttype)
            for line in value.splitlines(True):
                if color:
                    outfile.write(ansiformat(color, line.rstrip('\n')))
                else:
                    outfile.write(line.rstrip('\n'))
                if line.endswith('\n'):
                    if self.linenos:
                        self._write_lineno(outfile)
                    else:
                        outfile.write('\n')

        if self.linenos:
            outfile.write('\n')