# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-jqog4noo/pygments/pygments/formatters/irc.py
# Compiled at: 2016-12-29 05:31:34
# Size of source mod 2**32: 5775 bytes
"""
    pygments.formatters.irc
    ~~~~~~~~~~~~~~~~~~~~~~~

    Formatter for IRC output

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import sys
from pygments.formatter import Formatter
from pygments.token import Keyword, Name, Comment, String, Error, Number, Operator, Generic, Token, Whitespace
from pygments.util import get_choice_opt
__all__ = [
 'IRCFormatter']
IRC_COLORS = {Token: ('', ''), 
 Whitespace: ('lightgray', 'darkgray'), 
 Comment: ('lightgray', 'darkgray'), 
 Comment.Preproc: ('teal', 'turquoise'), 
 Keyword: ('darkblue', 'blue'), 
 Keyword.Type: ('teal', 'turquoise'), 
 Operator.Word: ('purple', 'fuchsia'), 
 Name.Builtin: ('teal', 'turquoise'), 
 Name.Function: ('darkgreen', 'green'), 
 Name.Namespace: ('_teal_', '_turquoise_'), 
 Name.Class: ('_darkgreen_', '_green_'), 
 Name.Exception: ('teal', 'turquoise'), 
 Name.Decorator: ('darkgray', 'lightgray'), 
 Name.Variable: ('darkred', 'red'), 
 Name.Constant: ('darkred', 'red'), 
 Name.Attribute: ('teal', 'turquoise'), 
 Name.Tag: ('blue', 'blue'), 
 String: ('brown', 'brown'), 
 Number: ('darkblue', 'blue'), 
 Generic.Deleted: ('red', 'red'), 
 Generic.Inserted: ('darkgreen', 'green'), 
 Generic.Heading: ('**', '**'), 
 Generic.Subheading: ('*purple*', '*fuchsia*'), 
 Generic.Error: ('red', 'red'), 
 Error: ('_red_', '_red_')}
IRC_COLOR_MAP = {'white': 0, 
 'black': 1, 
 'darkblue': 2, 
 'green': 3, 
 'red': 4, 
 'brown': 5, 
 'purple': 6, 
 'orange': 7, 
 'darkgreen': 7, 
 'yellow': 8, 
 'lightgreen': 9, 
 'turquoise': 9, 
 'teal': 10, 
 'lightblue': 11, 
 'darkred': 11, 
 'blue': 12, 
 'fuchsia': 13, 
 'darkgray': 14, 
 'lightgray': 15}

def ircformat(color, text):
    if len(color) < 1:
        return text
    else:
        add = sub = ''
        if '_' in color:
            add += '\x1d'
            sub = '\x1d' + sub
            color = color.strip('_')
        if '*' in color:
            add += '\x02'
            sub = '\x02' + sub
            color = color.strip('*')
        if len(color) > 0:
            add += '\x03' + str(IRC_COLOR_MAP[color]).zfill(2)
            sub = '\x03' + sub
        return add + text + sub
    return '<' + add + '>' + text + '</' + sub + '>'


class IRCFormatter(Formatter):
    __doc__ = '\n    Format tokens with IRC color sequences\n\n    The `get_style_defs()` method doesn\'t do anything special since there is\n    no support for common styles.\n\n    Options accepted:\n\n    `bg`\n        Set to ``"light"`` or ``"dark"`` depending on the terminal\'s background\n        (default: ``"light"``).\n\n    `colorscheme`\n        A dictionary mapping token types to (lightbg, darkbg) color names or\n        ``None`` (default: ``None`` = use builtin colorscheme).\n\n    `linenos`\n        Set to ``True`` to have line numbers in the output as well\n        (default: ``False`` = no line numbers).\n    '
    name = 'IRC'
    aliases = ['irc', 'IRC']
    filenames = []

    def __init__(self, **options):
        Formatter.__init__(self, **options)
        self.darkbg = get_choice_opt(options, 'bg', [
         'light', 'dark'], 'light') == 'dark'
        self.colorscheme = options.get('colorscheme', None) or IRC_COLORS
        self.linenos = options.get('linenos', False)
        self._lineno = 0

    def _write_lineno(self, outfile):
        self._lineno += 1
        outfile.write('\n%04d: ' % self._lineno)

    def _format_unencoded_with_lineno(self, tokensource, outfile):
        self._write_lineno(outfile)
        for ttype, value in tokensource:
            if value.endswith('\n'):
                self._write_lineno(outfile)
                value = value[:-1]
            color = self.colorscheme.get(ttype)
            while color is None:
                ttype = ttype[:-1]
                color = self.colorscheme.get(ttype)

            if color:
                color = color[self.darkbg]
                spl = value.split('\n')
                for line in spl[:-1]:
                    self._write_lineno(outfile)
                    if line:
                        outfile.write(ircformat(color, line[:-1]))

                if spl[(-1)]:
                    outfile.write(ircformat(color, spl[(-1)]))
            else:
                outfile.write(value)

        outfile.write('\n')

    def format_unencoded(self, tokensource, outfile):
        if self.linenos:
            self._format_unencoded_with_lineno(tokensource, outfile)
            return
        for ttype, value in tokensource:
            color = self.colorscheme.get(ttype)
            while color is None:
                ttype = ttype[:-1]
                color = self.colorscheme.get(ttype)

            if color:
                color = color[self.darkbg]
                spl = value.split('\n')
                for line in spl[:-1]:
                    if line:
                        outfile.write(ircformat(color, line))
                    outfile.write('\n')

                if spl[(-1)]:
                    outfile.write(ircformat(color, spl[(-1)]))
                else:
                    outfile.write(value)