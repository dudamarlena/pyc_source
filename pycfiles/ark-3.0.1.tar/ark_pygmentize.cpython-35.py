# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dmlhllnd/dev/src/ark/ark/ext/ark_pygmentize.py
# Compiled at: 2016-09-05 18:24:48
# Size of source mod 2**32: 1912 bytes
import html
try:
    import shortcodes
except ImportError:
    shortcodes = None

try:
    import pygments, pygments.lexers, pygments.formatters
except ImportError:
    pygments = None

if shortcodes:

    @shortcodes.register('code', 'endcode')
    def handler(record, content, pargs, kwargs):
        lang = pargs[0] if pargs else ''
        if pygments:
            code = pygmentize(content, lang)
        else:
            code = html.escape(content)
        if lang:
            fmt = '<pre class="lang-%s" data-lang="%s">\n%s\n</pre>'
            return fmt % (lang, lang, code.strip('\n'))
        else:
            return '<pre>\n%s\n</pre>' % code.strip('\n')


def pygmentize(code, lang):
    if lang:
        try:
            lexer = pygments.lexers.get_lexer_by_name(lang)
        except pygments.util.ClassNotFound:
            lexer = None

    else:
        try:
            lexer = pygments.lexers.guess_lexer(code)
        except pygments.util.ClassNotFound:
            lexer = None

        if lexer:
            formatter = pygments.formatters.HtmlFormatter(nowrap=True)
            return pygments.highlight(code, lexer, formatter)
        else:
            return html.escape(code)