# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mautrix/util/markdown.py
# Compiled at: 2019-11-21 01:01:47
# Size of source mod 2**32: 1093 bytes
import commonmark

class HtmlEscapingRenderer(commonmark.HtmlRenderer):

    def __init__(self, allow_html=False):
        super().__init__()
        self.allow_html = allow_html

    def lit(self, s):
        if self.allow_html:
            return super().lit(s)
        else:
            return super().lit(s.replace('<', '&lt;').replace('>', '&gt;'))

    def image(self, node, entering):
        prev = self.allow_html
        self.allow_html = True
        super().image(node, entering)
        self.allow_html = prev


md_parser = commonmark.Parser()
yes_html_renderer = commonmark.HtmlRenderer()
no_html_renderer = HtmlEscapingRenderer()

def render(message: str, allow_html: bool=False) -> str:
    parsed = md_parser.parse(message)
    if allow_html:
        return yes_html_renderer.render(parsed)
    else:
        return no_html_renderer.render(parsed)