# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/readme-renderer/readme_renderer/markdown.py
# Compiled at: 2019-07-30 18:47:11
# Size of source mod 2**32: 3039 bytes
from __future__ import absolute_import, division, print_function
import re, warnings, pygments, pygments.lexers, pygments.formatters
from six.moves import html_parser
from .clean import clean
_EXTRA_WARNING = "Markdown renderers are not available. Install 'readme_render[md]' to enable Markdown rendering."
try:
    import cmarkgfm
    variants = {'GFM':cmarkgfm.github_flavored_markdown_to_html, 
     'CommonMark':cmarkgfm.markdown_to_html}
except ImportError:
    warnings.warn(_EXTRA_WARNING)
    variants = {}

_LANG_ALIASES = {'python': 'python3'}

def render(raw, variant='GFM', **kwargs):
    if not variants:
        warnings.warn(_EXTRA_WARNING)
        return
    else:
        renderer = variants.get(variant)
        if not renderer:
            return
        rendered = renderer(raw)
        if not rendered:
            return
        highlighted = _highlight(rendered)
        cleaned = clean(highlighted)
        return cleaned


def _highlight(html):
    """Syntax-highlights HTML-rendered Markdown.

    Plucks sections to highlight that conform the the GitHub fenced code info
    string as defined at https://github.github.com/gfm/#info-string.

    Args:
        html (str): The rendered HTML.

    Returns:
        str: The HTML with Pygments syntax highlighting applied to all code
            blocks.
    """
    formatter = pygments.formatters.HtmlFormatter(nowrap=True)
    code_expr = re.compile('<pre><code class="language-(?P<lang>.+?)">(?P<code>.+?)</code></pre>', re.DOTALL)

    def replacer(match):
        try:
            lang = match.group('lang')
            lang = _LANG_ALIASES.get(lang, lang)
            lexer = pygments.lexers.get_lexer_by_name(lang)
        except ValueError:
            lexer = pygments.lexers.TextLexer()

        code = match.group('code')
        code = html_parser.HTMLParser().unescape(code)
        highlighted = pygments.highlight(code, lexer, formatter)
        return '<pre>{}</pre>'.format(highlighted)

    result = code_expr.sub(replacer, html)
    return result