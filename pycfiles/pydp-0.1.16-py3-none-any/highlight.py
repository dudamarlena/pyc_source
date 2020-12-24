# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pydozeoff/template/highlight.py
# Compiled at: 2010-03-18 23:00:33
__doc__ = '\nProvides functions to handle source code highlighting.\n'
from pygments import highlight
from pygments.lexers import get_lexer_by_name, PythonLexer
from pygments.formatters import HtmlFormatter
from pygments.styles import get_style_by_name
from pydozeoff.conf import settings

def get_style_defs(name='default'):
    """Returns the CSS code used to highlight source code. If the given style
    name isn't found, the default style will be used.
    """
    try:
        return HtmlFormatter(style=name).get_style_defs()
    except:
        return HtmlFormatter().get_style_defs()


def code(language, source_code):
    """Formats the given source code snippet as HTML.
    """
    formatter = HtmlFormatter(**settings['SYNTAX_HIGHLIGHT_OPTIONS'])
    return highlight(source_code, _get_lexer(language, source_code), formatter)


def _get_lexer(language, source_code):
    """Returns the appropriate lexer to parse the given source code snippet.
    """
    try:
        lexer = get_lexer_by_name(language)
    except:
        try:
            lexer = guess_lexer(source_code)
        except:
            lexer = PythonLexer()

    return lexer