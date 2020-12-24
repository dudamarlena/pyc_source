# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/redbaron/redbaron/syntax_highlight.py
# Compiled at: 2019-07-30 18:47:05
# Size of source mod 2**32: 1777 bytes
HAS_PYGMENTS = True
try:
    import pygments
except ImportError:
    HAS_PYGMENTS = False

if HAS_PYGMENTS:
    from pygments.token import Comment, Text, String, Keyword, Name, Operator, Generic
    from pygments.lexer import RegexLexer, bygroups
    from pygments import highlight
    from pygments.lexers import PythonLexer
    from pygments.formatters import Terminal256Formatter, HtmlFormatter

    class HelpLexer(RegexLexer):
        name = 'Lexer for RedBaron .help() method output'
        tokens = {'root': [
                  (
                   '\\x1b(.*?)\\[(\\d+)m', Generic),
                  (
                   '#.*$', Comment),
                  (
                   '(\'([^\\\\\']|\\\\.)*\'|\\"([^\\\\\\"]|\\\\.)*\\")', String),
                  (
                   '(None|False|True)', String),
                  (
                   '(\\*)( \\w+Node)', bygroups(Operator, Keyword)),
                  (
                   '\\w+Node', Name.Function),
                  (
                   '(\\*|=|->|\\(|\\)|\\.\\.\\.)', Operator),
                  (
                   '\\w+', Text),
                  (
                   '\\s+', Text)]}


    def help_highlight(string):
        return highlight(string, HelpLexer(), Terminal256Formatter(style='monokai'))


    def python_highlight(string):
        return highlight(string, PythonLexer(encoding='Utf-8'), Terminal256Formatter(style='monokai', encoding='Utf-8'))


    def python_html_highlight(string):
        return highlight(string, PythonLexer(encode='Utf-8'), HtmlFormatter(noclasses=True, encoding='UTf-8'))


else:

    def help_highlight(string):
        return string.encode('Utf-8')


    def python_highlight(string):
        return string.encode('Utf-8')


    def python_html_highlight(string):
        return string.encode('Utf-8')