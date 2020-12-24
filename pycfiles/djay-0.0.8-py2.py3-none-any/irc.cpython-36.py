# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/Pygments/pygments/formatters/irc.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 5869 bytes
"""
    pygments.formatters.irc
    ~~~~~~~~~~~~~~~~~~~~~~~

    Formatter for IRC output

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import sys
from pygments.formatter import Formatter
from pygments.token import Keyword, Name, Comment, String, Error, Number, Operator, Generic, Token, Whitespace
from pygments.util import get_choice_opt
__all__ = [
 'IRCFormatter']
IRC_COLORS = {Token: ('', ''), 
 Whitespace: ('gray', 'brightblack'), 
 Comment: ('gray', 'brightblack'), 
 Comment.Preproc: ('cyan', 'brightcyan'), 
 Keyword: ('blue', 'brightblue'), 
 Keyword.Type: ('cyan', 'brightcyan'), 
 Operator.Word: ('magenta', 'brightcyan'), 
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
 Generic.Error: ('brightred', 'brightred'), 
 Error: ('_brightred_', '_brightred_')}
IRC_COLOR_MAP = {'white':0, 
 'black':1, 
 'blue':2, 
 'brightgreen':3, 
 'brightred':4, 
 'yellow':5, 
 'magenta':6, 
 'orange':7, 
 'green':7, 
 'brightyellow':8, 
 'lightgreen':9, 
 'brightcyan':9, 
 'cyan':10, 
 'lightblue':11, 
 'red':11, 
 'brightblue':12, 
 'brightmagenta':13, 
 'brightblack':14, 
 'gray':15}

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


class IRCFormatter(Formatter):
    __doc__ = '\n    Format tokens with IRC color sequences\n\n    The `get_style_defs()` method doesn\'t do anything special since there is\n    no support for common styles.\n\n    Options accepted:\n\n    `bg`\n        Set to ``"light"`` or ``"dark"`` depending on the terminal\'s background\n        (default: ``"light"``).\n\n    `colorscheme`\n        A dictionary mapping token types to (lightbg, darkbg) color names or\n        ``None`` (default: ``None`` = use builtin colorscheme).\n\n    `linenos`\n        Set to ``True`` to have line numbers in the output as well\n        (default: ``False`` = no line numbers).\n    '
    name = 'IRC'
    aliases = ['irc', 'IRC']
    filenames = []

    def __init__(self, **options):
        (Formatter.__init__)(self, **options)
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
            else:
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