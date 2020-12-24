# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ditz/colorize.py
# Compiled at: 2019-01-11 11:03:55
"""
Output syntax highlighting.
"""
import sys
from .config import config
from .logger import log
try:
    from pygments import highlight
    from pygments.lexer import RegexLexer, bygroups
    from pygments.token import Text, Generic
    from pygments.styles import STYLE_MAP
    from pygments.formatters import NullFormatter, TerminalFormatter, Terminal256Formatter

    class DitzLexer(RegexLexer):
        """
        Interactive Ditz lexer.
        """
        name = 'Ditz'
        aliases = ['ditz', 'pyditz']
        tokens = {'root': [
                  (
                   '^Ditz:', Generic.Prompt),
                  (
                   '^-- More .+$', Generic.Prompt),
                  (
                   '[a-z]+-\\d+', Generic.Strong),
                  (
                   '(?<=\\()feature(?=\\))', Generic.Inserted),
                  (
                   '(?<=\\()bug(?=\\))', Generic.Deleted),
                  (
                   '(?<=\\* )bugfix(?=:)', Generic.Deleted),
                  (
                   '^\\d[^ \\n]+(?= \\()', Generic.Heading),
                  (
                   '^Unassigned', Generic.Heading),
                  (
                   '(?<=closed: )fixed', Generic.Inserted),
                  (
                   "(?<=closed: )won\\'t fix", Generic.Deleted),
                  (
                   '(?<=closed: )reorganized', Generic.Strong),
                  (
                   '^[A-Za-z ]{11}:', Generic.Subheading),
                  (
                   '[\\w.]+@[\\w.]+', Generic.Strong),
                  (
                   '^(== +)([^ ]+)( +/ +)(.+)$',
                   bygroups(Text, Generic.Heading, Text, Generic.Subheading)),
                  (
                   '^Error:', Generic.Error),
                  (
                   '.', Text)]}


    class DitzSessionLexer(RegexLexer):
        """
        Ditz output lexer.
        """
        name = 'Ditz session'
        aliases = ['ditzsession']
        tokens = {'root': [
                  (
                   '[_=>x] +[a-z]+-\\d+: .+$', Text),
                  (
                   '^( +Title|Description):.*$', Text),
                  (
                   '^(Start|Stopp|Comment|Add|Chang|Clos)ing.+$', Text),
                  (
                   '^([A-Z][^:?\\n]*[:?])(.*)$',
                   bygroups(Text, Generic.Strong)),
                  (
                   '^(>)(.*)$',
                   bygroups(Text, Generic.Strong)),
                  (
                   '.*\\n', Text)]}


    lexer = DitzLexer(encoding='utf-8', ensurenl=False)
    if sys.platform == 'win32':
        try:
            import colorama
            colorama.init()
            formatter = TerminalFormatter()
        except ImportError:
            formatter = NullFormatter()

    else:
        style = config.get('highlight', 'style')
        if style in STYLE_MAP:
            formatter = Terminal256Formatter(style=style)
        else:
            log.warning("'%s' is not a Pygments style" % style)
            formatter = NullFormatter()
    if not sys.stdout.isatty():
        formatter = NullFormatter()

    def colorize(text):
        return highlight(text, lexer, formatter)


except ImportError:

    def colorize(text):
        return text